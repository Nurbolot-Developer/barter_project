from typing import Any, Optional
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer
from .selectors import get_ads_filtered, get_all_exchange_proposals
from .services import create_ad, create_exchange_proposal

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        query: Optional[str] = self.request.query_params.get('q')
        return get_ads_filtered(query)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_all_exchange_proposals()

    def perform_create(self, serializer):
        proposal = create_exchange_proposal(serializer.validated_data, self.request.user)
        serializer.instance = proposal  # Обновляем инстанс сериализатора после создания