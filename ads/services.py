from typing import Dict
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal


def create_ad(data: Dict, user: User) -> Ad:
    """Создаёт объявление, привязывая его к пользователю."""
    ad = Ad.objects.create(user=user, **data)
    return ad

def create_exchange_proposal(data: Dict, user: User) -> ExchangeProposal:
    ad_sender = data.get('ad_sender')
    ad_receiver = data.get('ad_receiver')
    comment=data.get('message', '')
    status = data.get('status', 'pending')

    # Если ad_sender — ID, получить объект, иначе оставить как есть
    if isinstance(ad_sender, int):
        ad_sender = Ad.objects.get(id=ad_sender, user=user)
    if isinstance(ad_receiver, int):
        ad_receiver = Ad.objects.get(id=ad_receiver)

    if ad_sender.user != user:
        raise PermissionError("Пользователь не владеет объявлением отправителя.")

    proposal = ExchangeProposal.objects.create(
        ad_sender=ad_sender,
        ad_receiver=ad_receiver,
        proposer=user,
        comment=comment,
        status=status,
    )
    return proposal


