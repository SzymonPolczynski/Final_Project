from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from timetable.forms import AddUserForm, AddEmployeeForm, AddTeamForm
from timetable.models import User, Employee, Team


class MainPageView(View):
    def get(self, request):
        return render(request, "main_page.html")


class UserDetailsView(View):
    def get(self, request, user_id):
        ctx = {"user": get_object_or_404(User, pk=user_id)}
        return render(request, "user_details.html", ctx)


class AddUserView(View):
    def get(self, request):
        form = AddUserForm
        return render(request, "create_user.html", {"form": form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            user_lastname = form.cleaned_data["user_lastname"]
            user_email = form.cleaned_data["user_email"]
            phone = form.cleaned_data["phone"]
            city = form.cleaned_data["city"]
            street = form.cleaned_data["street"]
            postcode = form.cleaned_data["postcode"]
            new_user = User.objects.create(
                user_name=user_name,
                user_lastname=user_lastname,
                user_email=user_email,
                phone=phone,
                city=city,
                street=street,
                postcode=postcode,
            )
            return redirect(f"/user/{new_user.id}")
        return render(request, "create_user.html", {"form": form})


class EmployeeDetailsView(View):
    def get(self, request, employee_id):
        ctx = {"employee": get_object_or_404(Employee, pk=employee_id)}
        return render(request, "employee_details.html", ctx)


class AddEmployeeView(View):
    def get(self, request):
        form = AddEmployeeForm
        return render(request, "create_employee.html", {"form": form})

    def post(self, request):
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            employee_name = form.cleaned_data["employee_name"]
            employee_surname = form.cleaned_data["employee_surname"]
            job = form.cleaned_data["job"]
            new_employee = Employee.objects.create(
                employee_name=employee_name, employee_surname=employee_surname, job=job
            )
            return redirect(f"/employee/{new_employee.id}")
        return render(request, "create_employee.html", {"form": form})


class TeamDetailsView(View):
    def get(self, request, team_id):
        ctx = {"team": get_object_or_404(Team, pk=team_id)}
        return render(request, "team_details.html", ctx)


class AddTeamView(View):
    def get(self, request):
        form = AddTeamForm
        return render(request, "compose_team.html", {"form": form})

    def post(self, request):
        form = AddTeamForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data["team_name"]
            employees = form.cleaned_data["employees"]
            new_team = Team.objects.create(team_name=team_name, employees=employees)
            return redirect(f"/team/{new_team.id}")
        return render(request, "compose_team.html", {"form": form})


class AllUsersView(TemplateView):
    template_name = "all_users.html"

    def get_context_data(self):
        return {"users": User.objects.all()}


class DeleteUserView(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        message = "Usunięto użytkownika z bazy danych"
        user.delete()
        return render(request, "message.html", {"message": message})


class ModifyUserView(View):
    pass


class AllEmployeesView(TemplateView):
    template_name = "all_employees.html"

    def get_context_data(self):
        return {"employees": Employee.objects.all()}


class DeleteEmployeeView(View):
    def get(self, request, employee_id):
        employee = Employee.objects.get(pk=employee_id)
        message = "Usunięto pracownika z bazy danych"
        employee.delete()
        return render(request, "message.html", {"message": message})


class ModifyEmployeeView(View):
    pass


class AllTeamsView(TemplateView):
    template_name = "all_teams.html"

    def get_context_data(self):
        return {"teams": Team.objects.all()}


class DeleteTeamView(View):
    def get(self, request, team_id):
        team = Team.objects.get(pk=team_id)
        message = "Usunięto ekpię z bazy danych"
        team.delete()
        return render(request, "message.html", {"message": message})


class ModifyTeamView(View):
    pass
