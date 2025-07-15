import pytest
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal

@pytest.mark.django_db
def test_create_ad():
    user = User.objects.create_user(username='testuser', password='12345')
    ad = Ad.objects.create(
        user=user,
        title="Test Ad",
        description="Test Description",
        category="electronics",
        condition="used"
    )
    assert ad.id is not None
    assert ad.title == "Test Ad"

@pytest.mark.django_db
def test_update_ad():
    user = User.objects.create_user(username='testuser2', password='12345')
    ad = Ad.objects.create(
        user=user,
        title="Old Title",
        description="Old Desc",
        category="books",
        condition="new"
    )
    ad.title = "New Title"
    ad.save()
    updated_ad = Ad.objects.get(id=ad.id)
    assert updated_ad.title == "New Title"

@pytest.mark.django_db
def test_create_exchange_proposal():
    user = User.objects.create_user(username='testuser3', password='12345')
    ad1 = Ad.objects.create(user=user, title="Ad 1", description="Desc", category="tools", condition="new")
    ad2 = Ad.objects.create(user=user, title="Ad 2", description="Desc", category="tools", condition="used")
    proposal = ExchangeProposal.objects.create(
        ad_sender=ad1,
        ad_receiver=ad2,
        comment="Let's swap",
        status="ожидает"
    )
    assert proposal.id is not None
    assert proposal.status == "ожидает"
