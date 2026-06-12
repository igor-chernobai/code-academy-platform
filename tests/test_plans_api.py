import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_plans_api(api_client, basic_plan, pro_plan):
    url = reverse("api:plan_list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
