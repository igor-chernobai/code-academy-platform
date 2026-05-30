import pytest
from django.urls import reverse
from rest_framework import status

from users.models import StudentProgress


@pytest.mark.django_db
def test_guest_cannot_open_lesson(client, course, lesson):
    response = client.get(f'/api/course/{course.id}/lesson/{lesson.slug}/')

    assert response.status_code == 401


@pytest.mark.django_db
def test_user_without_subscription_cannot_open_lesson(auth_client, course, lesson):
    response = auth_client.get(f'/api/course/{course.id}/lesson/{lesson.slug}/')

    assert response.status_code == 403


@pytest.mark.django_db
def test_user_with_subscription_but_not_enrolled_cannot_open_lesson(auth_client_with_active_subscription, course):
    response = auth_client_with_active_subscription.get(f'/api/course/{course.id}/')

    assert response.status_code == 403


@pytest.mark.django_db
def test_user_with_subscription_and_enrolled_can_open_lesson(auth_client_with_active_subscription, user, course, module,
                                                             lesson):
    course.students.add(user)
    response = auth_client_with_active_subscription.get(f'/api/course/{course.id}/')

    assert response.status_code == 200
    assert response.data['title'] == lesson.title
    assert response.data['id'] == lesson.id


def test_student_can_complete_lesson(auth_client_with_active_subscription, user, lesson):
    url = reverse('api:lesson_complete', args=[lesson.id])
    response = auth_client_with_active_subscription.post(url)

    progress = StudentProgress.objects.get(student=user, lesson=lesson)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['lesson_id'] == lesson.id
    assert response.data['is_complete'] is True
    assert progress.student == user
    assert progress.is_complete is True


def test_guest_cannot_complete_lesson(api_client, lesson):
    url = reverse('api:lesson_complete', args=[lesson.id])
    response = api_client.post(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not StudentProgress.objects.filter(lesson=lesson).exists()


def test_student_without_subscription_cannot_complete_lesson(auth_client, lesson, user):
    url = reverse('api:lesson_complete', args=[lesson.id])
    response = auth_client.post(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not StudentProgress.objects.filter(lesson=lesson, student=user).exists()


def test_complete_lesson_twice_does_not_create_duplicate_progress(auth_client_with_active_subscription, lesson, user):
    url = reverse('api:lesson_complete', args=[lesson.id])

    auth_client_with_active_subscription.post(url)
    response = auth_client_with_active_subscription.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert StudentProgress.objects.filter(lesson=lesson, student=user).count() == 1


def test_student_cannot_complete_invalid_lesson(auth_client_with_active_subscription, user):
    url = reverse('api:lesson_complete', args=[9999])

    response = auth_client_with_active_subscription.post(url)

    assert response.status_code == 404
