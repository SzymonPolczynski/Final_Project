from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=64)
    user_lastname = models.CharField(max_length=64)
    user_email = models.CharField(max_length=128)
    phone = models.IntegerField()
    city = models.CharField(max_length=64, blank=True, null=True)
    street = models.CharField(max_length=128, blank=True, null=True)
    postcode = models.CharField(max_length=6, blank=True, null=True)


class TargetDate(models.Model):
    start_date = models.DateField()
    finish_date = models.DateField()
    periodically = models.BooleanField(default=False)


class Employee(models.Model):
    JOBS = (("Chief", "Chief"), ("Handyman", "Handyman"))
    employee_name = models.CharField(max_length=64)
    employee_surname = models.CharField(max_length=64)
    job = models.CharField(max_length=8, choices=JOBS)

    def __str__(self):
        return self.employee_name


class Team(models.Model):
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
    target_date = models.ManyToManyField(TargetDate)
    comments = models.TextField(null=True)


class Comments(models.Model):
    subject = models.CharField(max_length=128)
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE)
