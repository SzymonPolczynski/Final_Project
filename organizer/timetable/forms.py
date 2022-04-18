from django import forms
from .models import Employee, Team


class AddUserForm(forms.Form):
    user_name = forms.CharField(label="Imię", max_length=64)
    user_lastname = forms.CharField(label="Nazwisko", max_length=64)
    user_email = forms.CharField(label="Email", max_length=128)
    phone = forms.IntegerField(label="Numer telefonu")
    city = forms.CharField(label="Miasto", max_length=64, required=False)
    street = forms.CharField(label="Ulica", max_length=128, required=False)
    postcode = forms.CharField(label="Kod pocztowy", max_length=6, required=False)


class AddEmployeeForm(forms.Form):
    employee_name = forms.CharField(label="Imię", max_length=64)
    employee_surname = forms.CharField(label="Nazwisko", max_length=64)
    job = forms.ChoiceField(label="Funkcja", choices=Employee.JOBS)


class AddTeamForm(forms.Form):
    team_name = forms.CharField(label="Nazwa zespołu", max_length=64)
    employees = forms.ModelMultipleChoiceField(
        label="Dodaj pracowników do zespołu",
        queryset=Employee.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
