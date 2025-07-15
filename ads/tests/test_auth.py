import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_user_registration_success():
    client = APIClient()
    url = reverse('ads:register')

    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password1": "strongpassword123",
        "password2": "strongpassword123",
    }

    response = client.post(url, data)
    # Проверяем редирект после успешной регистрации
    assert response.status_code == 302
    # Можно проверить, что редирект на страницу логина
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_user_registration_duplicate_username():
    User.objects.create_user(username="testuser", password="pass")
    client = APIClient()
    url = reverse('ads:register')

    data = {
        "username": "testuser",
        "email": "another@example.com",
        "password1": "strongpassword123",
        "password2": "strongpassword123",
    }

    response = client.post(url, data)
    # При ошибке формы статус 200, т.к. рендерим страницу с ошибками
    assert response.status_code == 200
    # В теле страницы должно быть сообщение об ошибке (например, "ошибка" или "username")
    content = response.content.decode().lower()
    assert "error" in content or "ошибка" in content or "username" in content
