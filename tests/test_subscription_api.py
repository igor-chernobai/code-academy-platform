import pytest
from django.urls import reverse
from rest_framework import status

from subscriptions.models import Subscription


@pytest.mark.django_db
def test_auth_user_can_create_subscription(auth_client, user, basic_plan):
    url = reverse('api:subscription_create')
    response = auth_client.post(url, {'plan': basic_plan.id})
    subscription = Subscription.objects.get(student=user)

    assert response.status_code == status.HTTP_201_CREATED
    assert Subscription.objects.count() == 1
    assert subscription.student == user
    assert subscription.plan == basic_plan
    assert 'student' not in response.data
    assert 'plan' not in response.data
    assert 'plan_data' in response.data
    assert 'start_date' in response.data
    assert 'end_date' in response.data
    assert 'is_active' in response.data


@pytest.mark.django_db
def test_guest_cannot_create_subscription(api_client, basic_plan):
    url = reverse('api:subscription_create')
    response = api_client.post(url, {'plan': basic_plan.id})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Subscription.objects.count() == 0


@pytest.mark.parametrize(
    'plan_data',
    [
        ({'plan': None}),
        ({}),
        ({'plan': 'abc'}),
        ({'plan': ''}),
        ({'plan': 9999})
     ]
)
@pytest.mark.django_db
def test_subscription_create_with_invalid_plan_data(auth_client, plan_data):
    url = reverse('api:subscription_create')

    response = auth_client.post(url, plan_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Subscription.objects.count() == 0
    assert 'plan' in response.data
