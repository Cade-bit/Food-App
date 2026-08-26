from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "item_name", "item_description", "item_price", "item_image"]


class BulkDeleteSerializer(serializers.ModelSerializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )