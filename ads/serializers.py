from rest_framework import serializers
from .models import Ad, ExchangeProposal

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = [
            'id', 'user', 'title', 'city', 'description',
            'image_url', 'category', 'condition', 'price',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())
    ad_receiver = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())

    class Meta:
        model = ExchangeProposal
        fields = '__all__'
