import pytest
from courses.models import Course
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_guest_can_get_course_list(api_client, course):
    response = api_client.get('/api/courses/')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == course.id
    assert response.data[0]['title'] == course.title


@pytest.mark.django_db
def test_guest_can_get_course_detail(api_client, course):
    response = api_client.get(f'/api/courses/{course.id}/')

    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['about'] == course.about


@pytest.mark.django_db
def test_guest_get_not_found_course_detail(api_client):
    response = api_client.get('/api/courses/9999/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_guest_cannot_enroll_to_course(api_client, course):
    response = api_client.post(f'/api/courses/{course.id}/enroll/')

    assert response.status_code in [401, 403]


@pytest.mark.django_db
def test_user_without_subscription_cannot_enroll_to_course(auth_client, course, user):
    response = auth_client.post(f'/api/courses/{course.id}/enroll/')

    assert response.status_code == 403
    assert not course.students.filter(id=user.id).exists()
