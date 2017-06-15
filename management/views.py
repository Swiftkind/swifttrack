import calendar
import pytz
import decimal

from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import Account, Payroll
from projects.models import WorkDiary, Project, ProjectAssignment
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMessage, send_mail
from django.template.defaultfilters import slugify
from accounts.models import Account, Payroll
from projects.models import WorkDiary, Project, ProjectAssignment
from datetime import datetime, timedelta
from django.utils import timezone
from threading import Timer
from django.contrib.postgres.search import SearchQuery, SearchVector

from .forms import RequestForm, AddProjectForm, AssignEmployeeForm, EditProjectForm, EditProjectHoursForm
from .models import Requests
from .pdf import CreatePdf
from .utils import DateUtils, ProjectsUtils
from .mixins import StaffRequiredMixin


class RequestView(StaffRequiredMixin, TemplateView):

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

class UpdateRequest(StaffRequiredMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        id = request.POST['id']
        status = request.POST['status']
        confirmed = status or None
        Requests.objects.filter(id=id).update(confirmed=confirmed)
        return redirect('view_all_requests')


class AdminView(StaffRequiredMixin, TemplateView):

    permission_required = 'is_staff'
    template_name = 'management/workdiaries.html'

    def get(self, request, *args, **kwargs):
       
        date_requested = request.GET.get('prev_date') or request.GET.get('next_date')

        date_today = timezone.now().date()

        if not date_requested:
            date_requested = date_today - timedelta(days=1)

        wd_date = datetime.strptime(str(date_requested), '%Y-%m-%d').date()

        prev_date =wd_date - timedelta(days=1)
        next_date = wd_date + timedelta(days=1)

        work_diaries = WorkDiary.objects.filter(date__date=wd_date).order_by('-date')

        context = {
            'work_diaries': work_diaries,
            'prev_date': prev_date,
            'next_date': next_date,
            'date_today': date_today,
            'wd_date': wd_date
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        the_date = request.POST.get('wd_date')
        employee = request.POST.get('employee')

        if not employee:
            employee = Account.objects.values_list('id', flat=True).filter(is_staff=False)

        project = request.POST.get('project')

        if not project:
            project = Project.objects.values_list('id', flat=True)

        the_date = datetime.strptime(the_date, '%m/%d/%Y')


        work_diaries = WorkDiary.objects.filter(
            date__date=the_date
        ).filter(
            project_assignment__project__id__in=project
        ).filter(
            project_assignment__employee__id__in=employee
        ).order_by('-date')

        if type(project) is str:
            project = int(project)

        if type(employee) is str:
            employee = int(employee)

        return_data = {'work_diaries': work_diaries, 'wd_date': the_date,
            'return_today': True, 'employee_selected': employee, 'project_selected': project }
        
        return render(request, self.template_name, return_data)

class ConfirmAccountView(StaffRequiredMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirm') is not None:
            Account.objects.filter(id=request.POST['id']).update(is_active=True)
        if request.POST.get('decline') is not None:
            account = Account.objects.get(id=request.POST['id']).delete()
        return redirect('all_employees')

class DeactivateAccountView(StaffRequiredMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        Account.objects.filter(id=request.POST['id']).update(is_active=False)
        return redirect('admin', day=0)


class AllEmployeesView(StaffRequiredMixin, TemplateView):

    template_name = 'management/employees.html'

    def get(self, request, *args, **kwargs):
        all_employees = Account.objects.filter(is_active=True, is_staff=False)
        accounts_to_confirm = Account.objects.filter(is_active=False)
        return_data = {'all_employees': all_employees,
            'accounts_to_confirm': accounts_to_confirm}
        return render(request, self.template_name, return_data)

class EmployeeProfileView(StaffRequiredMixin, TemplateView):

    template_name = 'management/employee-profile.html'

    def get(self, request, *args, **kwargs):
        employee = Account.objects.get(id=kwargs['id'])
        return_data = {'employee': employee}
        return render(request, self.template_name, return_data)

class ViewRequestsView(StaffRequiredMixin, TemplateView):

    template_name = 'management/all-requests.html'

    def get(self, request, *args, **kwargs):
        all_requests = Requests.objects.all()
        return_data = {'all_requests': all_requests}
        return render(request, self.template_name, return_data)

class ProjectManageView(StaffRequiredMixin, TemplateView):

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

class ViewReportsByEmployee(StaffRequiredMixin, TemplateView):

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

class ManagementPayrollView(StaffRequiredMixin, TemplateView):
    template_name = 'management/payroll.html'

    def get(self, request, *args, **kwargs):
        date_now = datetime.now(pytz.utc)
        date_utils = DateUtils()
        date_sep = date_utils.get_year_month_day(date_now)
        last_day = calendar.monthrange(date_sep['get_year'],
            date_sep['get_month'])[1]
        employees = Account.objects.all().exclude(is_staff=True)
        all_payroll = Payroll.objects.all()
        return_data = {'payrolls': all_payroll}
        return render(request, self.template_name, return_data)

    def post(self, request, *args, **kwargs):
        payroll = Payroll.objects.get(id=request.POST['id'])
        instance = payroll
        instance.paid = request.POST['status']
        instance.date_paid = datetime.now(pytz.utc)
        instance.save()
        from_email = settings.EMAIL_HOST_USER
        to_email = [payroll.employee.email,]
        message = EmailMessage(
                'Payroll Confirmation',
                'We would like to inform you that your payroll has been successfully sent!',
                from_email,
                to_email,
            )
        message.attach_file('media/' + request.POST['invoice_file'])
        message.send()
        return redirect('management_payroll')

class AddProjectView(StaffRequiredMixin, TemplateView):

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

class AssignEmployeeView(StaffRequiredMixin, TemplateView):

    form_class = AssignEmployeeForm
    template = 'management/project-assign-employee.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id'))
        proj_id = kwargs['id']
        form = self.form_class(initial={'project': proj_id})
        ctx_data = {
            'form': form,
            'proj_id': proj_id,
            'project': project
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

class EditProjectView(StaffRequiredMixin, TemplateView):

    template_name = 'management/edit_project.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id'))
        assignments = ProjectAssignment.objects.filter(project=project)
        form = EditProjectForm(request.GET or None, instance=project)
        ctx_data = {
            'form': form,
            'project': project,
            'assignments': assignments
        }
        return render(request, self.template_name, ctx_data)

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id'))
        assignments = ProjectAssignment.objects.filter(project=project)
        form = EditProjectForm(request.POST or None, instance=project)
        if form.is_valid():
            form.save()
            return redirect('edit-project', id=kwargs.get('id'))
        ctx_data = {
            'form': form
        }
        return render (request, self.template_name, ctx_data)

class EditHoursView(StaffRequiredMixin, TemplateView):

    template_name = 'management/edit_project_hours.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('project_id'))
        weekly_hours = ProjectAssignment.objects.get(id=kwargs.get('id'), project=project)
        form = EditProjectHoursForm()
        ctx_data = {'form': form, 'weekly_hours': weekly_hours, 'project_id': project.id}
        return render(request, self.template_name, ctx_data)

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('project_id'))
        weekly_hours = ProjectAssignment.objects.get(id=kwargs.get('id'), project=project)
        form = EditProjectHoursForm(request.POST, instance=weekly_hours)
        if form.is_valid():
            form.save()
            return redirect('edit-project', id=kwargs.get('project_id'))
        ctx_data = {'form': form}
        return render(request, self.template_name, ctx_data)

class RemoveEmployee(StaffRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        employee_id = kwargs['employee_id']
        pa = ProjectAssignment.objects.get(project__id=project_id, employee__id=employee_id)
        pa.status = False
        pa.save() 
        return redirect('edit-project', id=kwargs.get('project_id'))

class ReAssignEmployee(StaffRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        employee_id = kwargs['employee_id']
        pa = ProjectAssignment.objects.get(project__id=project_id, employee__id=employee_id)
        pa.status = True
        pa.save() 
        return redirect('edit-project', id=kwargs.get('project_id'))


class AdminGlobalSearch(StaffRequiredMixin, TemplateView):

    template_name = 'management/search.html'

    def get(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        search_query = self.request.GET.get('q')

        context = {}
        
        if not search_query:
            messages.warning(self.request, 'Enter keywork to search')

        else:

            workdiaries = WorkDiary.objects.filter(
                Q(finished_task__icontains=search_query)
                | Q(todo_task__icontains=search_query)
                | Q(issues__icontains=search_query)
            ).order_by('-date')

            employees = Account.objects.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(about_me__icontains=search_query)
                | Q(address__icontains=search_query)
                | Q(contact_number__icontains=search_query)
            )

            requests = Requests.objects.filter(
                Q(subject__icontains=search_query)
                | Q(content__icontains=search_query)
            )

            payroll = Payroll.objects.filter(
                Q(description=search_query)
                | Q(invoice_file=search_query)
            )

            if 'search_workdiaries' not in context:
                context.update(
                    search_workdiaries=workdiaries
                )

            if 'search_employees' not in context:
                context.update(
                    search_employees=employees
                )

            if 'search_requests' not in context:
                context.update(
                    search_requests=requests
                )

            if 'search_payroll' not in context:
                context.update(
                    search_payroll=payroll
                )

        return render(self.request, self.template_name, context)