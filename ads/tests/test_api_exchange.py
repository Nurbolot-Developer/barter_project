import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad, ExchangeProposal

User = get_user_model()

@pytest.mark.django_db
def test_create_exchange_proposal_success():
    # Создаем пользователей
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')

    # Создаем объявления для обмена
    ad1 = Ad.objects.create(
        user=user1,
        title="Объявление 1",
        city="Город",
        description="Описание",
        category="other",
        condition="new"
    )
    ad2 = Ad.objects.create(
        user=user2,
        title="Объявление 2",
        city="Город",
        description="Описание",
        category="other",
        condition="used"
    )

    client = APIClient()
    client.force_authenticate(user=user1)

    data = {
        "ad_sender": ad1.id,       # Обязательно ID, а не объект
        "ad_receiver": ad2.id,     # Обязательно ID, а не объект
        "status": "pending",       # Если есть выбор статусов — используйте существующий
        # "comment": "Комментарий", # по желанию
    }

    # Проверка, что передаются ID, а не объекты
    assert isinstance(data['ad_sender'], int), "ad_sender должен быть числом (ID объявления)"
    assert isinstance(data['ad_receiver'], int), "ad_receiver должен быть числом (ID объявления)"

    url = reverse('exchangeproposal-list')  # Проверьте, что это корректный роут для вашего viewset
    response = client.post(url, data, format='json')

    assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.data}"
