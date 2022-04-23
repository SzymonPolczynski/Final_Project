from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, UpdateView, FormView

from timetable.forms import (
    AddUserForm,
    AddEmployeeForm,
    AddTeamForm,
    AddUserReservationForm,
    LoginForm,
    SignUpForm,
    AddServiceForm,
)
from timetable.models import CustomUser, Employee, Team, Services, Reservation


class MainPageView(View):
    """
    Displays landing page for application.
    """

    def get(self, request):
        return render(request, "main_page.html")


class AddUserView(View):
    """
    Creates new user and saves it in database.
    """

    def get(self, request):
        form = SignUpForm
        return render(request, "create_user.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        return render(request, "create_user.html", {"form": form})


class UserDetailsView(LoginRequiredMixin, View):
    """
    Displays user details for currently logged user.
    """

    def get(self, request, user_id):
        customer = CustomUser.objects.get(pk=user_id)
        if user_id == request.user.id:
            ctx = {"customer": customer}
            return render(request, "user_details.html", ctx)
        else:
            return HttpResponseForbidden()


class AllUsersView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """
    Displays list of all users in database. Staff permission is needed.
    """

    permission_required = "is_staff"
    template_name = "all_users.html"

    def get_context_data(self):
        return {"users": CustomUser.objects.filter(is_superuser=False)}


class DeleteUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Deletes user from database. Staff permission is needed.
    """

    permission_required = "is_staff"

    def get(self, request, user_id):
        user = CustomUser.objects.get(pk=user_id)
        message = "Usunięto użytkownika z bazy danych"
        user.delete()
        return render(request, "message.html", {"message": message})


class ModifyUserView(LoginRequiredMixin, UpdateView):
    """
    Enables data modification for currently logged user.
    """

    model = CustomUser
    fields = ["first_name", "last_name", "email", "phone", "city", "street", "postcode"]
    template_name = "modify_user.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.id != self.request.user.id:
            return redirect(obj)
        return super(ModifyUserView, self).dispatch(request, *args, **kwargs)


class AddUserReservationView(LoginRequiredMixin, View):
    """
    Creating new reservation in database for currently logged user.
    """

    def get(self, request):
        form = AddUserReservationForm
        return render(request, "make_reservation.html", {"form": form})

    def post(self, request):
        form = AddUserReservationForm(request.POST)
        if form.is_valid():
            new_reservation = form.save(commit=False)
            new_reservation.customer = CustomUser.objects.get(pk=request.user.id)
            new_reservation.save()
            return redirect(f"/reservation/{new_reservation.id}")
        return render(request, "make_reservation.html", {"form": form})


class UserReservationDetailsView(LoginRequiredMixin, View):
    """
    Displays reservation details for specific reservation.
    """

    def get(self, request, reservation_id):
        ctx = {"reservation": Reservation.objects.get(pk=reservation_id)}
        return render(request, "reservation_details.html", ctx)


class AllUserReservationsView(LoginRequiredMixin, View):
    """
    Displays all reservation for currently logged user.
    Divides reservations into pending for acceptance and one that already accepted.
    """

    def get(self, request, user_id):
        user = CustomUser.objects.get(pk=user_id)
        reservations = Reservation.objects.filter(customer=user, is_accepted=False)
        accepted_reservations = Reservation.objects.filter(
            customer=user, is_accepted=True
        )
        return render(
            request,
            "user_reservations_details.html",
            {
                "reservations": reservations,
                "accepted_reservations": accepted_reservations,
            },
        )


class AddEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Creates new employee and saves it in database. Staff permission is needed.
    """

    permission_required = "is_staff"

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


class EmployeeDetailsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Displays employee details. Staff permission is needed.
    """

    permission_required = "is_staff"

    def get(self, request, employee_id):
        ctx = {"employee": get_object_or_404(Employee, pk=employee_id)}
        return render(request, "employee_details.html", ctx)


class AllEmployeesView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """
    Displays list of all employees. Staff permission is needed.
    """

    permission_required = "is_staff"
    template_name = "all_employees.html"

    def get_context_data(self):
        return {"employees": Employee.objects.all()}


class DeleteEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Deletes employee from database. Staff permission is needed.
    """

    permission_required = "is_staff"

    def get(self, request, employee_id):
        employee = Employee.objects.get(pk=employee_id)
        message = "Usunięto pracownika z bazy danych"
        employee.delete()
        return render(request, "message.html", {"message": message})


class ModifyEmployeeView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Enables data modification for selected employee. Staff permission is needed.
    """

    permission_required = "is_staff"
    model = Employee
    fields = ["employee_name", "employee_surname", "job"]
    template_name = "modify_employee.html"


class AddTeamView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Creates new team and saves it in database. Staff permission is needed.
    """

    permission_required = "is_staff"

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


class TeamDetailsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Displays team details. Staff permission is needed.
    """

    permission_required = "is_staff"

    def get(self, request, team_id):
        ctx = {"team": get_object_or_404(Team, pk=team_id)}
        return render(request, "team_details.html", ctx)


class AllTeamsView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """
    Displays list of all teams. Staff permission is needed.
    """

    permission_required = "is_staff"
    template_name = "all_teams.html"

    def get_context_data(self):
        return {"teams": Team.objects.all()}


class DeleteTeamView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Deletes team from database. Staff permission is needed.
    """

    permission_required = "is_staff"

    def get(self, request, team_id):
        team = Team.objects.get(pk=team_id)
        message = "Usunięto ekipę z bazy danych"
        team.delete()
        return render(request, "message.html", {"message": message})


class ModifyTeamView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Enables data modification for selected team. Staff permission is needed.
    """

    permission_required = "is_staff"
    model = Team
    fields = ["team_name", "employees"]
    template_name = "modify_team.html"


class AddServiceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Creates new service and saves it in database. Staff permission is needed.
    """

    permission_required = "is_staff"

    def get(self, request):
        form = AddServiceForm
        return render(request, "create_service.html", {"form": form})

    def post(self, request):
        form = AddServiceForm(request.POST)
        if form.is_valid():
            service_name = form.cleaned_data["service_name"]
            Services.objects.create(service_name=service_name)
            return redirect("/all-services/")
        return render(request, "create_service.html", {"form": form})


class DeleteServiceView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Deletes service from database. Staff permission is needed.
    """

    permission_required = "is_staff"

    def get(self, request, service_id):
        service = Services.objects.get(pk=service_id)
        message = "Usunięto usługę z bazy danych"
        service.delete()
        return render(request, "message.html", {"message": message})


class AllServicesView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """
    Displays list of all services. Staff permission is needed.
    """

    permission_required = "is_staff"
    template_name = "all_services.html"

    def get_context_data(self):
        return {"services": Services.objects.all()}


class AllReservationsView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """
    Displays list of all reservations. Staff permission is needed.
    """

    permission_required = "is_staff"
    template_name = "all_reservations.html"

    def get_context_data(self):
        return {
            "reservations": Reservation.objects.filter(is_accepted=False),
            "accepted_reservations": Reservation.objects.filter(is_accepted=True),
        }


class ManageReservationView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Enables Staff user to accept and assign team for selected reservation. Staff permission is needed.
    """

    permission_required = "is_staff"
    model = Reservation
    fields = [
        "customer",
        "teams",
        "target_date",
        "comments",
        "is_accepted",
        "service_type",
    ]
    template_name = "manage_reservation.html"


class CheckReservationView(View):
    """
    Provides date boolean JsonResponse for selected service type.
    Main functionality is to check if there is free date for current service.
    """

    def get(self, request, date, service):
        service_obj = Services.objects.get(pk=service)
        reservation = Reservation.objects.filter(
            target_date=date, service_type=service_obj
        )
        if reservation:
            return JsonResponse({"is_available": False})
        else:
            return JsonResponse({"is_available": True})


class LoginView(View):
    """
    Displays login panel.
    """

    def get(self, request):
        form = LoginForm()
        return render(request, "login_form.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(email=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("index"))
            user = CustomUser.objects.filter(email=username)
            if user:
                message = "Nieprawidłowy login lub hasło"
                form = LoginForm()
                ctx = {"form": form, "message": message}
                return render(request, "login_form.html", ctx)
            return redirect("/add-user/")

        else:
            ctx = {"form": form}
            return render(request, "login_form.html", ctx)


class LogoutView(LoginRequiredMixin, View):
    """
    Redirects to mains page after user logs out.
    """

    def get(self, request):
        logout(request)
        return redirect(reverse("index"))
