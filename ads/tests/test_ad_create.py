import pytest
from ads.models import Ad
from django.contrib.auth.models import User  # стандартная модель User в Django

@pytest.mark.django_db
def test_create_ad_success():
    user = User.objects.create_user(username="testuser", password="password123")
    
    ad = Ad.objects.create(
        user=user,
        title="Ноутбук",
        description="Игровой ноутбук",
        city="Бишкек",
        category="Электроника"
    )

    assert ad.id is not None
    assert ad.title == "Ноутбук"
    assert ad.description == "Игровой ноутбук"
    assert ad.city == "Бишкек"
    assert ad.category == "Электроника"
    assert ad.user == user
