import pytest
from django.contrib.auth import get_user_model

from ads.models import Ad, ExchangeProposal
from ads import services

User = get_user_model()


@pytest.mark.django_db
def test_create_ad_success():
    user = User.objects.create_user(username='testuser', password='password123')
    data = {
        'title': 'Тестовое объявление',
        'description': 'Описание',
        'city': 'Бишкек',
        'category': 'Электроника',
        # 'image' исключаем, если в модели его нет или оно необязательное
    }

    ad = services.create_ad(data, user)

    assert ad.id is not None
    assert ad.title == data['title']
    assert ad.description == data['description']
    assert ad.city == data['city']
    assert ad.category == data['category']
    assert ad.user == user


@pytest.mark.django_db
def test_create_exchange_proposal_success():
    user = User.objects.create_user(username='testuser', password='password123')

    ad_sender = Ad.objects.create(
        user=user,
        title='Ad 1',
        description='desc 1',
        city='Osh',
        category='Книги'
    )
    ad_receiver = Ad.objects.create(
        user=user,
        title='Ad 2',
        description='desc 2',
        city='Bishkek',
        category='Книги'
    )

    data = {
        'ad_sender': ad_sender,
        'ad_receiver': ad_receiver,
        'message': 'Готов обменяться!',
    }

    proposal = services.create_exchange_proposal(data, user)

    assert proposal.id is not None
    assert proposal.ad_sender == ad_sender
    assert proposal.ad_receiver == ad_receiver
    assert proposal.proposer == user  # поле proposer должно быть в модели
    assert proposal.comment == data['message']
    assert proposal.status == 'pending'
