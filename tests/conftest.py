import pytest
from courses.models import Course
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course(db):
    return Course.objects.create(
        title="Python Backend",
        slug="python-backend",
        short_description="Learn backend",
        about="Full course description",
    )
