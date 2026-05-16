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
