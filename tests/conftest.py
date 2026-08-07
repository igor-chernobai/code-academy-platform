import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from courses.models import Course, Lesson, Module
from subscriptions.models import Plan
from subscriptions.services.subscription import subscription_create


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user("testuser@gmail.com", "12345789")


@pytest.fixture
def auth_client(user, api_client):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def auth_client_with_active_subscription(user, api_client):
    api_client.force_authenticate(user=user)
    plan = Plan.objects.create(name="Test Plan", price=9999, features="Test", duration_days=30)
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


@pytest.fixture
def module(db, course):
    return Module.objects.create(
        course=course,
        title="Django Basics",
        slug="django-basics",
        note="Basic Django module",
        order=1,
    )


@pytest.fixture
def lesson(db, module):
    return Lesson.objects.create(
        module=module,
        title="Introduction to Django",
        slug="introduction-to-django",
        content="Lesson content",
        order=1,
    )


@pytest.fixture
def another_course():
    return Course.objects.create(
        title="Django Advanced",
        slug="django-advanced",
        short_description="Advanced Django",
        about="Full course description",
    )


@pytest.fixture
def basic_plan():
    return Plan.objects.create(
        name="Basic Plan", price=500, features="Test features", duration_days=30
    )


@pytest.fixture
def pro_plan():
    return Plan.objects.create(
        name="Professional Plan", price=3000, features="Test features", duration_days=365
    )
