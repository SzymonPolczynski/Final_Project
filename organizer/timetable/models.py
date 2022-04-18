from django.db import models
from django.urls import reverse


class User(models.Model):
    user_name = models.CharField(max_length=64)
    user_lastname = models.CharField(max_length=64)
    user_email = models.CharField(max_length=128)
    phone = models.IntegerField()
    city = models.CharField(max_length=64, blank=True, null=True)
    street = models.CharField(max_length=128, blank=True, null=True)
    postcode = models.CharField(max_length=6, blank=True, null=True)

    @property
    def name(self):
        return "{} {}".format(self.user_name, self.user_lastname)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user-details', kwargs={'user_id': self.pk})


class TargetDate(models.Model):
    start_date = models.DateField()
    finish_date = models.DateField()
    periodically = models.BooleanField(default=False)


class Employee(models.Model):
    JOBS = (("Chief", "Chief"), ("Handyman", "Handyman"))
    employee_name = models.CharField(max_length=64)
    employee_surname = models.CharField(max_length=64)
    job = models.CharField(max_length=8, choices=JOBS)

    @property
    def name(self):
        return "{} {}".format(self.employee_name, self.employee_surname)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('employee-details', kwargs={'employee_id': self.pk})


class Team(models.Model):
    team_name = models.CharField(max_length=64)
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.team_name

    def get_absolute_url(self):
        return reverse('team-details', kwargs={'team_id': self.pk})


class Services(models.Model):
    service_name = models.CharField(max_length=128)


class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
    target_date = models.ManyToManyField(TargetDate)
    comments = models.TextField(null=True)
    is_accepted = models.BooleanField(default=False)
    service_type = models.ForeignKey(Services, on_delete=models.CASCADE)


class Comments(models.Model):
    subject = models.CharField(max_length=128)
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE)
