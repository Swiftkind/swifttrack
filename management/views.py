import calendar
import pytz
import decimal

from threading import Timer
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage, send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.views.generic import TemplateView, View
from django.views import generic
from threading import Timer
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


from .forms import (RequestForm,
                    AddProjectForm,
                    AssignEmployeeForm,
                    EditProjectForm,
                    EditProjectHoursForm,
                    AddMiscForm,
                    )
from .models import Requests, Misc
from .pdf import CreatePdf
from .utils import DateUtils, ProjectsUtils
from .mixins import StaffRequiredMixin
from accounts.models import Account, AccountLog, Payroll
from accounts.forms import UserProfileForm
from projects.models import WorkDiary, Project, ProjectAssignment



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

    def __init__(self, *args, **kwargs):
        super(AdminView, self).__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AdminView, self).get_context_data(*args, **kwargs)

        date_requested = self.request.GET.get('prev_date') or self.request.GET.get('next_date')

        date_today = timezone.now().date()

        if not date_requested:
            date_requested = date_today - timedelta(days=1)

        wd_date = datetime.strptime(str(date_requested), '%Y-%m-%d').date()

        prev_date = wd_date - timedelta(days=1)
        next_date = wd_date + timedelta(days=1)
        wd_hours = 0
        work_diaries = WorkDiary.objects.filter(date__date=wd_date
            ).order_by('-date')

        for work_diary in work_diaries:
            wd_hours += work_diary.hours

        context = {
            'work_diaries': work_diaries,
            'prev_date': prev_date,
            'next_date': next_date,
            'date_today': date_today,
            'wd_date': wd_date,
            'wd_hours': wd_hours,
        }
        return context


class AdminSearchView(StaffRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'management/workdiaries.html'

    def __init__(self, *args, **kwargs):
        super(AdminSearchView, self).__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AdminSearchView, self).get_context_data(*args, **kwargs)

        employee = self.request.GET.get('employee')
        project = self.request.GET.get('project')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')

        date_today = timezone.now().date()

        if not start and not end:
            date_range = [date_today, date_today + timedelta(days=1)]
        else:
            date_range = [start, end]

        if not employee:
            employee = Account.objects.values_list('id', flat=True).filter(is_staff=False)

        if not project:
            project = Project.objects.values_list('id', flat=True)

        work_diaries = WorkDiary.objects.filter(date__range=date_range
            ).filter(project_assignment__project__id__in=project
            ).filter(project_assignment__employee__id__in=employee
            ).order_by('-date')

        if type(project) is str:
            project = int(project)

        if type(employee) is str:
            employee = int(employee)

        context = {
            'work_diaries': work_diaries,
            'employee_selected': employee,
            'project_selected': project,
            'go_back': True
        }
        return context


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
        ctx_data = {'works': works, 'project': project}
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
                       'project_assignments': project_assignments}
        return render(request, self.template_name, return_data)


class ManagementPayrollView(StaffRequiredMixin, TemplateView):
    template_name = 'management/payroll.html'

    def get(self, request, *args, **kwargs):
        date_now = timezone.now().date()
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
        instance.date_paid = timezone.now().date()
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
    template_name = 'management/project-add.html'

    def get(self, request, *args, **kwargs):
        form = AddProjectForm(initial={'user': request.user.id})
        ctx_data = {'form': form}
        return render(request, self.template_name, ctx_data)

    def post(self, request, *args, **kwargs):
        form = AddProjectForm(request.POST)
        if form.is_valid():
            form.save()
            project_id = form.instance.id
            return redirect('view_projects', project_id)


class AssignEmployeeView(StaffRequiredMixin, TemplateView):
    template_name = 'management/project-assign-employee.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id'))
        assigned = ProjectAssignment.objects.filter(project=project)
        accounts_list = assigned.values_list('employee_id', flat=True)
        accounts = Account.objects.exclude(id__in=accounts_list)
        form = AssignEmployeeForm()
        ctx_data = {'form': form, 'project': project, 'accounts': accounts}
        return render(request, self.template_name, ctx_data)

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id'))
        assigned = ProjectAssignment.objects.filter(project=project)
        accounts_list = assigned.values_list('employee_id', flat=True)
        accounts = Account.objects.exclude(id__in=accounts_list)
        form = AssignEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_projects', id=kwargs.get('id'))
        ctx_data = {'form': form, 'project': project, 'accounts': accounts}
        return render(request, self.template_name, ctx_data)


class EditProjectView(StaffRequiredMixin, TemplateView):
    template_name = 'management/edit_project.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id'))
        assignments = ProjectAssignment.objects.filter(project=project)
        form = EditProjectForm(request.GET or None, instance=project)
        ctx_data = {'form': form, 'project': project,
                    'assignments': assignments}
        return render(request, self.template_name, ctx_data)

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('id'))
        assignments = ProjectAssignment.objects.filter(project=project)
        form = EditProjectForm(request.POST or None, instance=project)
        if form.is_valid():
            form.save()
            return redirect('edit-project', id=kwargs.get('id'))
        ctx_data = {'form': form}
        return render (request, self.template_name, ctx_data)


class EditHoursView(StaffRequiredMixin, TemplateView):
    template_name = 'management/edit_project_hours.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs.get('project_id'))
        weekly_hours = ProjectAssignment.objects.get(id=kwargs.get('id'), project=project)
        form = EditProjectHoursForm()
        ctx_data = {'form': form, 'weekly_hours': weekly_hours,
                    'project_id': project.id}
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


class AttendanceView(TemplateView):
    """List attendance records"""

    def __init__(self, *args, **kwargs):
        super(AttendanceView, self).__init__(*args, **kwargs)

    template_name = 'management/attendance.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AttendanceView, self).get_context_data(**kwargs)

        date_requested = self.request.GET.get('prev_date') or self.request.GET.get('next_date')

        date_today = timezone.now().date()

        if not date_requested:
            date_requested = date_today

        attendance_date = datetime.strptime(str(date_requested), '%Y-%m-%d').date()

        prev_date =attendance_date - timedelta(days=1)
        next_date = attendance_date + timedelta(days=1)

        account_logs = AccountLog.objects.filter(date_created__date=attendance_date).order_by('-date_created')

        context = {
            'account_logs': account_logs,
            'prev_date': prev_date,
            'next_date': next_date,
            'date_today': date_today,
            'attendance_date': attendance_date
        }

        return context


class AttendanceSearchView(TemplateView):
    """AttendanceSearchView"""

    template_name = 'management/attendance.html'

    def __init__(self, *args, **kwargs):
        super(AttendanceSearchView, self).__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AttendanceSearchView, self).get_context_data(**kwargs)

        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        employee = self.request.GET.get('employee')

        date_today = timezone.now().date()

        if not start and not end:
            date_range = [date_today, date_today + timedelta(days=1)]
        else:
            date_range = [start, end]

        if not employee:
            employee = Account.objects.values_list('id', flat=True).filter(is_staff=False)

        account_logs = AccountLog.objects.filter(
            date_created__range=date_range
        ).filter(account__id__in=employee).order_by('-date_created')

        if type(employee) is str:
            employee = int(employee)

        context = {
            'account_logs': account_logs,
            'employee_selected': employee,
            'go_back': True
        }

        return context


class ProjectListView(TemplateView):
    template_name = 'management/projects_list.html'

    def get(self, request, *args, **kwargs):
        project_list = Project.objects.all().order_by('name')
        return render(request, self.template_name, {'project_list': project_list})


class ArchiveProjectView(StaffRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        pr = Project.objects.get(id=project_id)
        pr.status = False
        pr.save()
        return redirect('project-list')


class UnArchiveProjectView(StaffRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        pr = Project.objects.get(id=project_id)
        pr.status = True
        pr.save()
        return redirect('project-list')


class ProfileAdminView(StaffRequiredMixin, TemplateView):
    template_name = 'management/profile.html'

    def get(self, *args, **kwargs):
        form = UserProfileForm(instance=self.request.user)
        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        form = UserProfileForm(self.request.POST, self.request.FILES, instance=self.request.user)
        if form.is_valid():
            form.save()
        return redirect('admin')

class ChangePasswordView(TemplateView):
    template_name = 'management/change_password.html'

    def get(self, *args, **kwargs):
        form = PasswordChangeForm(user=self.request.user)
        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        form = PasswordChangeForm(data=self.request.POST, user=self.request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(self.request, form.user)
            return redirect('admin')
        ctx_data = {'form': form}
        return render(self.request, self.template_name, ctx_data)


class MiscView(StaffRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'management/misc.html'

    def get(self, *args, **kwargs):
        employees = Account.objects.all().exclude(is_staff=True)
        miscs = Misc.objects.filter(employees__in=employees)[:5]
        ctx_data = {'miscs': miscs}
        return render(self.request, self.template_name, ctx_data)


class AddMiscView(StaffRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'management/add_misc.html'

    def get(self, *args, **kwargs):
        form = AddMiscForm()
        ctx_data = {'form': form}
        return render(self.request, self.template_name, ctx_data)

    def post(self, *args, **kwargs):
        form = AddMiscForm(self.request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_misc')
        return render(self.request, self.template_name, {'form': form})


class ArchiveMiscView(StaffRequiredMixin, View):

    def get(self, *args, **kwargs):
        misc_id = kwargs['misc_id']
        ma = Misc.objects.get(id=misc_id)
        ma.status = False
        ma.save()
        return redirect('admin_misc')


class UnArchiveMiscView(StaffRequiredMixin, View):

    def get(self, *args, **kwargs):
        misc_id = kwargs['misc_id']
        ma = Misc.objects.get(id=misc_id)
        ma.status = True
        ma.save()
        return redirect('admin_misc')


class EditMiscView(StaffRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'management/edit_misc.html'

    def get(self, *args, **kwargs):
        misc_id = kwargs['misc_id']
        miscs = Misc.objects.get(id=misc_id)
        form = AddMiscForm(instance=miscs)
        ctx_data = {'form': form, 'miscs': miscs}
        return render(self.request, self.template_name, ctx_data)

    def post(self, *args, **kwargs):
        misc_id = kwargs['misc_id']
        miscs = Misc.objects.get(id=misc_id)
        form = AddMiscForm(self.request.POST, instance=miscs)
        if form.is_valid():
            form.save()
            return redirect('admin_misc')
        return render(self.request, self.template_name, {'form': form})


class MiscEmployeeView(StaffRequiredMixin, TemplateView):
    template_name = 'management/employee_misc.html'

    def get(self, *args, **kwargs):
        misc_id = kwargs['misc_id']
        miscs = Misc.objects.get(id=misc_id)
        ctx_data = {'miscs': miscs}
        return render(self.request, self.template_name, ctx_data)
