import pytest


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


@pytest.mark.django_db
def test_user_with_subscription_can_enroll_to_course(auth_client_with_active_subscription, course, user):
    response = auth_client_with_active_subscription.post(f'/api/courses/{course.id}/enroll/')

    assert response.status_code == 201
    assert course.students.filter(id=user.id).exists()
    assert response.data['course'] == course.title
    assert response.data['enroll'] is True


@pytest.mark.django_db
def test_guest_cannot_get_my_courses(client):
    response = client.get('/api/courses/my_courses/')

    assert response.status_code == 401


@pytest.mark.django_db
def test_user_without_subscription_cannot_get_my_courses(auth_client):
    response = auth_client.get('/api/courses/my_courses/')

    assert response.status_code == 403


@pytest.mark.django_db
def test_user_with_subscription_can_get_only_own_courses(auth_client_with_active_subscription, course, another_course,
                                                         user):
    course.students.add(user)
    response = auth_client_with_active_subscription.get('/api/courses/my_courses/')

    courses_id = [item['id'] for item in response.data['student_courses']]

    assert response.status_code == 200
    assert len(response.data['student_courses']) == 1
    assert response.data['student_courses'][0]['id'] == course.id
    assert another_course.id not in courses_id
