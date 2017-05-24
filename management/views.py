import calendar
import pytz
import decimal

from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import Account, Payroll
from projects.models import WorkDiary, Project, ProjectAssignment
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template.defaultfilters import slugify
from accounts.models import Account, Payroll
from projects.models import WorkDiary, Project, ProjectAssignment
from datetime import datetime, timedelta
from threading import Timer

from .forms import RequestForm, AddProjectForm, AssignEmployeeForm
from .models import Requests
from .forms import RequestForm, AddProjectForm, AssignEmployeeForm
from .models import Requests
from .pdf import CreatePdf
from .utils import DateUtils, ProjectsUtils

# Create your views here.


class RequestView(TemplateView):

    template_name = 'management/request.html'

    def get(self, request, *args, **kwargs):
        form = RequestForm(initial={'employee': request.user.id})
        requests_by_user = Requests.objects.filter(
            employee=request.user.id).order_by('-date_requested')
        return_data = {'form': form, 'requests_by_user': requests_by_user}
        return render(request, self.template_name, return_data)

    def post(self, request, *args, **kwargs):
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            form = RequestForm()
            requests_by_user = Requests.objects.filter(
                employee=request.user.id)
        return redirect('request')


class UpdateRequest(TemplateView):

    def post(self, request, *args, **kwargs):
        id = request.POST['id']
        status = request.POST['status']
        confirmed = status or None
        Requests.objects.filter(id=id).update(confirmed=confirmed)
        return redirect('view_all_requests')


class AdminView(TemplateView):

    template_name = 'management/workdiaries.html'

    def get(self, request, *args, **kwargs):
        day_diff = int(kwargs['day'])
        date_today = datetime.now() - timedelta(days=day_diff)
        previous_day = day_diff + 1
        if day_diff is 0:
            next_day = 0
        next_day = day_diff - 1
        work_diaries = WorkDiary.objects.filter(
            date__date=date_today).order_by('-date')
        return_data = {'work_diaries': work_diaries,
                'date_now': date_today, 'previous_day': previous_day,
                'next_day': next_day}
        return render(request, self.template_name, return_data)

    def post(self, request, *args, **kwargs):
        day_diff = int(kwargs['day'])
        the_date = request.POST.get('getDiariesByDate')
        the_date = datetime.strptime(the_date, '%m/%d/%Y')
        work_diaries = WorkDiary.objects.filter(date__date=the_date)
        return_data = {'work_diaries': work_diaries, 'date_now': the_date,
            'return_today': True}
        return render(request, self.template_name, return_data)


class ConfirmAccountView(TemplateView):

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirm') is not None:
            Account.objects.filter(id=request.POST['id']).update(is_active=True)
        if request.POST.get('decline') is not None:
            account = Account.objects.get(id=request.POST['id']).delete()
        return redirect('all_employees')


class DeactivateAccountView(TemplateView):

    def post(self, request, *args, **kwargs):
        Account.objects.filter(id=request.POST['id']).update(is_active=False)
        return redirect('admin', day=0)


class AllEmployeesView(TemplateView):

    template_name = 'management/employees.html'

    def get(self, request, *args, **kwargs):
        all_employees = Account.objects.filter(is_active=True)
        accounts_to_confirm = Account.objects.filter(is_active=False)
        return_data = {'all_employees': all_employees,
            'accounts_to_confirm': accounts_to_confirm}
        return render(request, self.template_name, return_data)


class EmployeeProfileView(TemplateView):

    template_name = 'management/employee-profile.html'

    def get(self, request, *args, **kwargs):
        employee = Account.objects.get(id=kwargs['id'])
        return_data = {'employee': employee}
        return render(request, self.template_name, return_data)


class ViewRequestsView(TemplateView):

    template_name = 'management/all-requests.html'

    def get(self, request, *args, **kwargs):
        all_requests = Requests.objects.all()
        return_data = {'all_requests': all_requests}
        return render(request, self.template_name, return_data)


class ProjectManageView(TemplateView):

    template_name = 'management/project.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id'))
        assignment = ProjectAssignment.objects.filter(project=project)
        works = WorkDiary.objects.filter(
            project_assignment__in=assignment).order_by('-date')
        page = self.request.GET.get('page', 1)
        query = request.GET.get('q')
        if query:
            works = works.filter(
                Q(finished_task__icontains=query)|
                Q(todo_task__icontains=query)|
                Q(issues__icontains=query)|
                Q(date__icontains=query)|
                Q(hours__icontains=query)
                ).distinct()
        paginator = Paginator(works, 2)
        try:
            works = paginator.page(page)
        except PageNotAnInteger:
            works = paginator.page(1)
        except EmptyPage:
            works = paginator.page(paginator.num_pages)
        ctx_data = {
            'works': works,
            'project': project,
        }
        return render(request, self.template_name, ctx_data)


class ViewReportsByEmployee(TemplateView):

    template_name = 'management/reports_by_employee.html'

    def get(self, request, *args, **kwargs):

        emp = Account.objects.get(id=kwargs['emp_id'])
        project_assignments = ProjectAssignment.objects.filter(
            employee=kwargs['emp_id'])
        page = self.request.GET.get('page', 1)
        paginator = Paginator(project_assignments, 10)
        try:
            project_assignments = paginator.page(page)
        except PageNotAnInteger:
            project_assignments = paginator.page(1)
        except EmptyPage:
            project_assignments = paginator.page(paginator.num_pages)
        projects = []
        for project in project_assignments:
            projects.append(project.id)
        reports = WorkDiary.objects.filter(
            project_assignment__in=projects).order_by('-date')
        return_data = {'reports': reports, 'employee': emp,
                       'project_assignments': project_assignments, }
        return render(request, self.template_name, return_data)


class ManagementPayrollView(TemplateView):
    template_name = 'management/payroll.html'

    def get(self, request, *args, **kwargs):
        '''1. Create payroll record
        '''
        date_now = datetime.now(pytz.utc)
        date_utils = DateUtils()
        date_sep = date_utils.get_year_month_day(date_now)
        last_day = calendar.monthrange(date_sep['get_year'],
            date_sep['get_month'])[1]
        employees = Account.objects.all().exclude(is_staff=True)
        if date_sep['get_day'] is 15 or date_sep['get_day'] is last_day:
            if Payroll.objects.filter(
                    date__date=date_now.date()).exists() is not True:
                for emp in employees:
                    '''2. Get total hours of employee for the period and
                    generate the invoice
                    '''
                    projects_utils = ProjectsUtils()
                    projects = projects_utils.get_employee_projects_assignments(
                        emp.id)
                    date_from = date_utils.get_start_date(date_now)
                    diaries = WorkDiary.objects.filter(
                        project_assignment__in=projects,
                        date__date__gte=date_from,
                        date__date__lte=date_now)
                    total_hours = decimal.Decimal(0)
                    for diary in diaries:
                        total_hours = total_hours + decimal.Decimal(diary.hours)
                    '''3. Get payroll record and generate the invoice
                    '''
                    AMOUNT_BEFORE_DEDUCTIONS = total_hours * emp.hourly_rate
                    PAYROLL_DESCRIPTION = 'Salary for the month'
                    # Prepare requirements for pdf creation
                    data = {'fname': emp.first_name, 'lname': emp.last_name,
                            'amount': AMOUNT_BEFORE_DEDUCTIONS,
                            'description': PAYROLL_DESCRIPTION,
                            'period': date_now.date(),
                            'total_hours': total_hours}
                    template = 'management/payroll-report.html'
                    file_path = 'payroll/' + \
                        slugify('{} {} {}'.format(emp.first_name,
                            emp.last_name, date_now.date()))+'.pdf'
                    style = 'h3 {font-size: 18px; font-weight: bold; }' + \
                        'h4 {font-size: 16px; font-weight: bold}'
                    create_pdf = CreatePdf()
                    payroll_report = create_pdf.generate_pdf(data, template,
                        file_path, style)
                    #Save payroll record
                    payroll = Payroll(
                        date=date_now,
                        employee=emp,
                        amount_before_deductions=AMOUNT_BEFORE_DEDUCTIONS,
                        description=PAYROLL_DESCRIPTION,
                        paid=False,
                        invoice_file=file_path
                    )
                    payroll.save()
        #Now return the payroll records
        all_payroll = Payroll.objects.all()
        return_data = {'payrolls': all_payroll}
        return render(request, self.template_name, return_data)

    def post(self, request, *args, **kwargs):
        Payroll.objects.filter(id=request.POST['id']).update(
            paid=request.POST['status'], date_paid=datetime.now(pytz.utc))
        #Send an email to the employee after confirming the payroll
        message = EmailMessage(
            'Payroll confirmation',
            'Hi! Your payroll is successfully confirmed! You may view or' + \
            'download it from the attachment. Thank you.',
            'gergimarjohnalinsangao@gmail.com',
            ['fantanhoj_ramiger@ymail.com']
        )
        message.attach_file('media/' + request.POST['invoice_file'])
        message.send()
        return redirect('management_payroll')


class AddProjectView(TemplateView):

    form_class = AddProjectForm
    template_name = 'management/project-add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'user': request.user.id})
        ctx_data = {
            'form': form,
        }
        return render(request, self.template_name, ctx_data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            p = form.save()
            return redirect('view_projects', id=p.id)
        ctx_data = {
            'form': form,
            'error': 'Can\'t add project',
        }
        return render(request, self.template_name, ctx_data)


class AssignEmployeeView(TemplateView):

    form_class = AssignEmployeeForm
    template = 'management/project-assign-employee.html'

    def get(self, request, *args, **kwargs):
        proj_id = kwargs['id']
        form = self.form_class(initial={'project': proj_id})
        ctx_data = {
            'form': form,
            'proj_id': proj_id,
        }
        return render(request, 'management/project-assign-employee.html', ctx_data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            employee = request.POST.get('employee')
            project = request.POST.get('project')
            assigned = ProjectAssignment.objects.filter(
                employee=employee, project=project).exists()
            if assigned:
                error = 'Employee is already assigned to this project.'
            else:
                form.save()
                return redirect('view_projects', id=kwargs.get('id'))
        ctx_data = {
            'form': form,
            'error': error,
        }
        return render(request, 'management/project-assign-employee.html', ctx_data)