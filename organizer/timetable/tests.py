import pytest
from django.test import TestCase, Client
from http import HTTPStatus

from django.urls import reverse

from timetable.models import CustomUser, Team, Services, Reservation


def test_main_page():
    """
    Tests landing page.
    """
    c = Client()
    response = c.get("")
    assert response.status_code == 200
    assert "Witamy na stronie głównej" in str(response.content, "utf-8")


def test_login_view():
    """
    Tests login view.
    """
    c = Client()
    response = c.get("/login/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_user():
    """
    Tests creating new user.
    """
    c = Client()
    response = c.get("/add-user/")
    assert response.status_code == 200
    response = c.post("/add-user/", data={"x": "a"})
    assert response.status_code == 200
    response = c.post(
        "/add-user/",
        data={
            "first_name": "a",
            "last_name": "b",
            "email": "a@b.com",
            "phone": "123456789",
            "city": "a",
            "street": "ab 1",
            "postcode": "12-345",
        },
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_detail():
    """
    Tests displaying user details for currently logged user.
    """
    c = Client()
    user = CustomUser.objects.create_user(email="user@user.com", password="123")
    url = reverse("user-details", kwargs={"user_id": user.id})
    response = c.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_reservation():
    """
    Tests creating new reservation.
    This tests both valid and invalid form.
    """
    u = CustomUser.objects.create_user(email="user@user.com", password="123")
    s = Services.objects.create(service_name="abc")
    c = Client()
    c.login(email="user@user.com", password="123")
    response = c.get("/reservation/")
    assert response.status_code == 200
    response = c.post(
        "/reservation/",
        data={"target_date": "2022-04-24", "comments": "abc", "service_type": 1},
    )
    assert response.status_code == 302  # when form is valid
    r = Reservation.objects.first()
    assert r is not None
    response = c.post(
        "/reservation/",
        data={"target_date": "abc", "comments": "abc", "service_type": 1},
    )
    assert response.status_code == 200  # when form is not valid
