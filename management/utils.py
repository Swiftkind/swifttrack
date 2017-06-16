from datetime import datetime
from projects.models import ProjectAssignment

class DateUtils():
    def get_year_month_day(self, date):
        the_day = date.day
        the_month = date.month
        the_year = date.year
        return {'get_day': the_day, 'get_month': the_month, 'get_year': the_year}

    def get_start_date(self, date):
        the_date = self.get_year_month_day(date)
        the_day = the_date['get_day']
        if the_day is 15:
            date_from = datetime(the_date['get_year'], the_date['get_month'], 1)
        else:
            date_from = datetime(the_date['get_year'], the_date['get_month'], 16)
        return date_from.date()

    #convert date to yyyy-mm-dd
    def convert_date(date_req):
        return datetime.strptime(str(date_req), '%Y-%m-%d').date()


class ProjectsUtils():
    def get_employee_projects_assignments(self, emp_id):
        project_assignments = ProjectAssignment.objects.filter(employee=emp_id)
        projects = []
        for project in project_assignments:
            projects.append(project.id)
        return projects
