from django.db import models
from .ad import Ad
from .base import TimeStampedModel
from django.conf import settings

class ExchangeProposal(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('declined', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals')
    proposer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='proposals_made',
        null=True  # временно добавляем null
    )
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Proposal from {self.ad_sender} to {self.ad_receiver}"
