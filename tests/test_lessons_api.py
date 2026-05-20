import pytest


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
