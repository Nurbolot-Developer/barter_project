import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.mark.django_db
def test_create_ad_success():
    user = User.objects.create_user(username='testuser', password='testpass')
    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "title": "Тестовое объявление",
        "description": "Описание объявления",
        "category": "electronics",
        "condition": "new",
        "city": "Москва",
    }

    url = reverse('ad-list')

    response = client.post(url, data, format='json')

    assert response.status_code == 201

