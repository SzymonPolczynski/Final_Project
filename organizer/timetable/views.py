from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, UpdateView, FormView

from timetable.forms import AddUserForm, AddEmployeeForm, AddTeamForm, AddUserReservationForm, LoginForm, SignUpForm
from timetable.models import User, Employee, Team, Services, Reservation


class MainPageView(View):
    def get(self, request):
        return render(request, "main_page.html")


class UserDetailsView(View):
    def get(self, request, user_id):
        ctx = {"user": get_object_or_404(User, pk=user_id)}
        return render(request, "user_details.html", ctx)


class AddUserView(View):
    def get(self, request):
        form = SignUpForm
        return render(request, "create_user.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
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
            employees_set = Employee.objects.filter(pk__in=employees)
            new_team = Team.objects.create(team_name=team_name)
            new_team.employees.set(employees_set)
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


class ModifyUserView(UpdateView):
    model = User
    fields = ["user_name", "user_lastname", "email", "phone", "city", "street", "postcode"]
    template_name = "modify_user.html"


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


class ModifyEmployeeView(UpdateView):
    model = Employee
    fields = ["employee_name", "employee_surname", "job"]
    template_name = "modify_employee.html"


class AllTeamsView(TemplateView):
    template_name = "all_teams.html"

    def get_context_data(self):
        return {"teams": Team.objects.all()}


class DeleteTeamView(View):
    def get(self, request, team_id):
        team = Team.objects.get(pk=team_id)
        message = "Usunięto ekipę z bazy danych"
        team.delete()
        return render(request, "message.html", {"message": message})


class ModifyTeamView(UpdateView):
    model = Team
    fields = ["team_name", "employees"]
    template_name = "modify_team.html"


class AddUserReservationView(View):
    def get(self, request):
        form = AddUserReservationForm
        return render(request, "make_reservation.html", {"form": form})

    def post(self, request):
        form = AddUserReservationForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data["customer"]
            target_date = form.cleaned_data["target_date"]
            comments = form.cleaned_data["comments"]
            service_type = form.cleaned_data["service_type"]
            customer_id = User.objects.get(pk=customer.id)
            service_type_id = Services.objects.get(pk=service_type.id)
            new_reservation = Reservation.objects.create(customer=customer_id, target_date=target_date,
                                                         comments=comments, service_type=service_type_id)
            return redirect(f"/reservation/{new_reservation.id}")
        return render(request, "make_reservation.html", {"form": form})


class UserReservationDetailsView(View):
    def get(self, request, reservation_id):
        ctx = {"reservation": get_object_or_404(Reservation, pk=reservation_id)}
        return render(request, "reservation_details.html", ctx)


class AllReservationsView(TemplateView):  # TODO tylko dla employee
    template_name = "all_reservations.html"

    def get_context_data(self):
        return {"reservations": Reservation.objects.filter(is_accepted=False),
                "accepted_reservations": Reservation.objects.filter(is_accepted=True)}


class ManageReservationView(UpdateView):
    model = Reservation
    fields = ["customer", "teams", "target_date", "comments", "is_accepted", "service_type"]
    template_name = "manage_reservation.html"


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login_form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(email=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
            user = User.objects.filter(email=username)
            if user:
                message = 'Nieprawidłowy login lub hasło'
                form = LoginForm()
                ctx = {'form': form, 'message': message}
                return render(request, 'login_form.html', ctx)
            return redirect('/add-user/')

        else:
            ctx = {'form': form}
            return render(request, 'login_form.html', ctx)


class LogoutView(View):
    def get(self, request):
        return render(request, "logout.html")

    def post(self, request):
        logout(request)
        return redirect(reverse("index"))
