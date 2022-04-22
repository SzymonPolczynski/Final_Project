from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from timetable.managers import UserManager


# class User(models.Model):
#     user_name = models.CharField(max_length=64)
#     user_lastname = models.CharField(max_length=64)
#     email = models.EmailField(max_length=128)
#     phone = models.IntegerField()
#     city = models.CharField(max_length=64, blank=True, null=True)
#     street = models.CharField(max_length=128, blank=True, null=True)
#     postcode = models.CharField(max_length=6, blank=True, null=True)
#
#     @property
#     def name(self):
#         return "{} {}".format(self.user_name, self.user_lastname)
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('user-details', kwargs={'user_id': self.pk})


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=15, blank=True, verbose_name=_('Numer telefonu'))
    city = models.CharField(max_length=64, blank=True, verbose_name=_('Miasto'))
    street = models.CharField(max_length=128, blank=True, verbose_name=_('Ulica'))
    postcode = models.CharField(max_length=6, blank=True, verbose_name=_('Kod pocztowy'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user-details', kwargs={'user_id': self.pk})


# class TargetDate(models.Model):
#     start_date = models.DateField()
#     finish_date = models.DateField()
#     periodically = models.BooleanField(default=False)


class Employee(models.Model):
    JOBS = (("Chief", "Brygadzista"), ("Handyman", "Pracownik fizyczny"))
    employee_name = models.CharField(max_length=64, verbose_name=_('Imię'))
    employee_surname = models.CharField(max_length=64, verbose_name=_('Nazwisko'))
    job = models.CharField(max_length=8, choices=JOBS, verbose_name=_('Funkcja'))

    @property
    def name(self):
        return "{} {}".format(self.employee_name, self.employee_surname)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('employee-details', kwargs={'employee_id': self.pk})


class Team(models.Model):
    team_name = models.CharField(max_length=64, verbose_name=_('Nazwa zespołu'))
    employees = models.ManyToManyField(Employee, verbose_name=_('Pracownicy'))

    def __str__(self):
        return self.team_name

    def get_absolute_url(self):
        return reverse('team-details', kwargs={'team_id': self.pk})


class Services(models.Model):
    service_name = models.CharField(max_length=128, verbose_name=_('Nazwa usługi'))

    def __str__(self):
        return self.service_name


class Reservation(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('Klient'))
    teams = models.ManyToManyField(Team, verbose_name=_('Ekipa'))
    target_date = models.DateField(verbose_name=_('Termin wykonania'))
    comments = models.TextField(null=True, verbose_name=_('Uwagi'))
    is_accepted = models.BooleanField(default=False, verbose_name=_('Zaakceptowano'))
    service_type = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name=_('Rodzaj usługi'))

    def get_absolute_url(self):
        return reverse('reservation-details', kwargs={'reservation_id': self.pk})


class Comments(models.Model):
    subject = models.CharField(max_length=128)
    content = models.TextField()
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE)
