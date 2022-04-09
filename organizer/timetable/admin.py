from django.contrib import admin
from .models import (User,
                     TargetDate,
                     Employee,
                     Team,
                     Reservation,
                     Comments)

admin.site.register(User)
admin.site.register(TargetDate)
admin.site.register(Employee)
admin.site.register(Team)
admin.site.register(Reservation)
admin.site.register(Comments)
