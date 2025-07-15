import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ads.models import Ad

@pytest.mark.django_db
def test_ad_list_api():
    client = APIClient()
    response = client.get('/api/ads/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_ad_create_api():
    user = User.objects.create_user(username='testuser', password='pass123')
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post('/api/ads/', {
        'title': 'Тест',
        'description': 'Описание',
        'city': 'Бишкек',
        'category': 'books',
        'condition': 'new',
    }, format='json')
    
    print(response.data)
    assert response.status_code == 201
    assert Ad.objects.count() == 1

@pytest.mark.django_db
def test_ad_detail_api():
    user = User.objects.create_user(username='testuser', password='pass123')
    ad = Ad.objects.create(
        user=user,
        title='Тест',
        description='Описание',
        city='Бишкек',
        category='books',
        condition='new'
    )
    client = APIClient()
    response = client.get(f'/api/ads/{ad.id}/')
    assert response.status_code == 200
    assert response.data['title'] == 'Тест'

@pytest.mark.django_db
def test_ad_update_api():
    user = User.objects.create_user(username='testuser', password='pass123')
    ad = Ad.objects.create(
        user=user,
        title='Старое',
        description='Описание',
        city='Бишкек',
        category='books',
        condition='new'

    )
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.patch(f'/api/ads/{ad.id}/', {'title': 'Новое'}, format='json')
    assert response.status_code == 200
    ad.refresh_from_db()
    assert ad.title == 'Новое'

@pytest.mark.django_db
def test_ad_delete_api():
    user = User.objects.create_user(username='testuser', password='pass123')
    ad = Ad.objects.create(
        user=user,
        title='Удалить',
        description='desc',
        city='Бишкек',
        category='books',
        condition='new'
    )
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.delete(f'/api/ads/{ad.id}/')
    assert response.status_code == 204
    assert Ad.objects.count() == 0

@pytest.mark.django_db
def test_unauthenticated_ad_create_fails():
    client = APIClient()
    response = client.post('/api/ads/', {
        'title': 'Без авторизации',
        'description': '...',
        'city': 'Бишкек',
        'category': 'books',
        'condition': 'new',
    }, format='json')
    assert response.status_code == 401  # Unauthorized

@pytest.mark.django_db
def test_ad_update_by_owner():
    user = User.objects.create_user(username='owner', password='pass123')
    ad = Ad.objects.create(
        user=user,
        title='Старое название',
        description='Описание',
        city='Бишкек',
        category='books',
        condition='new'
    )
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.patch(f'/api/ads/{ad.id}/', {'title': 'Новое название'}, format='json')
    assert response.status_code == 200
    ad.refresh_from_db()
    assert ad.title == 'Новое название'


@pytest.mark.django_db
def test_ad_update_by_non_owner_fails():
    owner = User.objects.create_user(username='owner', password='pass123')
    other_user = User.objects.create_user(username='other', password='pass123')

    ad = Ad.objects.create(
        user=owner,
        title='Чужое объявление',
        description='Описание',
        city='Бишкек',
        category='books',
        condition='new'
    )
    client = APIClient()
    client.force_authenticate(user=other_user)

    response = client.patch(f'/api/ads/{ad.id}/', {'title': 'Взлом!'}, format='json')
    assert response.status_code == 403  # Forbidden
    ad.refresh_from_db()
    assert ad.title == 'Чужое объявление'

