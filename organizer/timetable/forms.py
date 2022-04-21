from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Employee, Team, Reservation, CustomUser


class AddUserForm(forms.Form):
    user_name = forms.CharField(label="Imię", max_length=64)
    user_lastname = forms.CharField(label="Nazwisko", max_length=64)
    email = forms.CharField(label="Email", max_length=128)
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


class AddUserReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["target_date", "comments", "service_type"]
        widgets = {'target_date': forms.DateInput(format='%m/%d/%Y',
                                                  attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                         'type': 'date'})}


class LoginForm(forms.Form):
    username = forms.EmailField(label="Adres email", max_length=64)
    password = forms.CharField(
        label="Hasło", max_length=64, widget=forms.PasswordInput
    )


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'city',
                  'street', 'postcode', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Imię'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Nazwisko'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Numer telefonu'})
        self.fields['city'].widget.attrs.update({'placeholder': 'Miasto'})
        self.fields['street'].widget.attrs.update({'placeholder': 'Ulica'})
        self.fields['postcode'].widget.attrs.update({'placeholder': 'Kod pocztowy'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Hasło'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Powtórz hasło'})
        self.fields['phone'].label = "Numer telefonu"
        self.fields['city'].label = "Miasto"
        self.fields['street'].label = "Ulica"
        self.fields['postcode'].label = "Kod pocztowy"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
