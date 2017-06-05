import calendar
import pytz
import decimal

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib import messages

from management.utils import DateUtils, ProjectsUtils
from management.pdf import CreatePdf
from accounts.models import Payroll, Account
from projects.models import WorkDiary

class Command(BaseCommand):

    def handle(self, *args, **options):
        date_now = datetime.now(pytz.utc)
        date_utils = DateUtils()
        projects_utils = ProjectsUtils()
        date_sep = date_utils.get_year_month_day(date_now)
        last_day = calendar.monthrange(date_sep['get_year'],
            date_sep['get_month'])[1]
        employees = Account.objects.all().exclude(is_staff=True)
        if date_sep['get_day'] is 15 or date_sep['get_day'] is last_day:
            if Payroll.objects.filter(
                    date__date=date_now.date()).exists() is not True:
                for emp in employees:
                    projects = projects_utils.get_employee_projects_assignments(emp.id)
                    date_from = date_utils.get_start_date(date_now)
                    diaries = WorkDiary.objects.filter(
                        project_assignment__in=projects,
                        date__date__gte=date_from,
                        date__date__lte=date_now)
                    total_hours = decimal.Decimal(0)
                    for diary in diaries:
                        total_hours = total_hours + decimal.Decimal(diary.hours)
                    AMOUNT_BEFORE_DEDUCTIONS = total_hours * emp.hourly_rate
                    PAYROLL_DESCRIPTION = 'Salary for the month'
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
                    payroll = Payroll(
                        date=date_now,
                        employee=emp,
                        amount_before_deductions=AMOUNT_BEFORE_DEDUCTIONS,
                        description=PAYROLL_DESCRIPTION,
                        paid=False,
                        invoice_file=file_path
                    )
                    payroll.save()