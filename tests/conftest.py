import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from courses.models import Course
from subscriptions.models import Plan
from subscriptions.services.subscription import subscription_create


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user("testuser", "12345789")


@pytest.fixture
def auth_client(user, api_client):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def auth_client_with_active_subscription(user, api_client):
    api_client.force_authenticate(user=user)
    plan = Plan.objects.create(
        name="Test Plan", price=9999, features="Test", duration_days=30
    )
    subscription_create(student=user, plan=plan)
    return api_client


@pytest.fixture
def course(db):
    return Course.objects.create(
        title="Python Backend",
        slug="python-backend",
        short_description="Learn backend",
        about="Full course description",
    )
