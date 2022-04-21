"""organizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from timetable.views import (
    MainPageView,
    AddUserView,
    AddEmployeeView,
    AddTeamView,
    UserDetailsView,
    EmployeeDetailsView,
    TeamDetailsView,
    AllUsersView,
    DeleteUserView,
    ModifyUserView,
    AllEmployeesView,
    DeleteEmployeeView,
    ModifyEmployeeView,
    AllTeamsView,
    DeleteTeamView,
    ModifyTeamView,
    AddUserReservationView,
    UserReservationDetailsView,
    AllReservationsView,
    ManageReservationView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", MainPageView.as_view(), name="index"),
    path("add-user/", AddUserView.as_view(), name="add-user"),
    path("add-employee/", AddEmployeeView.as_view(), name="add-employee"),
    path("add-team/", AddTeamView.as_view(), name="add-team"),
    path("user/<int:user_id>/", UserDetailsView.as_view(), name="user-details"),
    path(
        "employee/<int:employee_id>/",
        EmployeeDetailsView.as_view(),
        name="employee-details",
    ),
    path("team/<int:team_id>/", TeamDetailsView.as_view(), name="team-details"),
    path('all-users/', AllUsersView.as_view(), name="all-users"),
    path('user/delete/<int:user_id>/', DeleteUserView.as_view(), name="delete-user"),
    path('user/modify/<int:pk>/', ModifyUserView.as_view(), name="modify-user"),
    path('all-employees/', AllEmployeesView.as_view(), name="all-employees"),
    path('employee/delete/<int:employee_id>/', DeleteEmployeeView.as_view(), name="delete-employee"),
    path('employee/modify/<int:pk>/', ModifyEmployeeView.as_view(), name="modify-employee"),
    path('all-teams/', AllTeamsView.as_view(), name="all-teams"),
    path('team/delete/<int:team_id>/', DeleteTeamView.as_view(), name="delete-team"),
    path('team/modify/<int:pk>/', ModifyTeamView.as_view(), name="modify-team"),
    path('reservation/', AddUserReservationView.as_view(), name="reservation"),
    path('reservation/<int:reservation_id>/', UserReservationDetailsView.as_view(), name="reservation-details"),
    path('all-reservations/', AllReservationsView.as_view(), name="all-reservations"),
    path('reservation/manage/<int:pk>/', ManageReservationView.as_view(), name="manage-reservation"),
    # path('')
]
