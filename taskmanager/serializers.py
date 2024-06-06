from rest_framework import serializers
from .models import ScrapedData


class CoinListSerializer(serializers.Serializer):
    coins = serializers.ListField(child=serializers.CharField())


class ScrapingStatusSerializer(serializers.Serializer):
    job_id = serializers.UUIDField()
    status = serializers.CharField()
    data = serializers.DictField()


class ScrapedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = '__all__'
