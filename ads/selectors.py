from typing import Optional
from django.db.models import QuerySet
from .models import Ad, ExchangeProposal
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def get_all_ads() -> QuerySet[Ad]:
    return Ad.objects.all()

def get_ads_filtered(query: Optional[str]) -> QuerySet[Ad]:
    qs = Ad.objects.all()
    if query:
        qs = qs.filter(title__icontains=query)
    return qs

def get_all_exchange_proposals() -> QuerySet[ExchangeProposal]:
    return ExchangeProposal.objects.all()

def get_user_ads_except(ad_id: int, user: User) -> QuerySet[Ad]:
    return Ad.objects.filter(user=user).exclude(id=ad_id)


def get_ad_by_id(ad_id: int) -> Ad:
    return get_object_or_404(Ad, id=ad_id)

