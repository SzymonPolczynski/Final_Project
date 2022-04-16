from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from timetable.forms import AddUserForm, AddEmployeeForm, AddTeamForm
from timetable.models import User, Employee


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
                employee_name=employee_name,
                employee_surname=employee_surname,
                job=job
            )
            return redirect(f"/employee/{new_employee.id}")
        return render(request, "create_employee.html", {"form": form})


class AddTeamView(View):
    def get(self, request):
        form = AddTeamForm
        return render(request, "compose_team.html", {"form": form})
