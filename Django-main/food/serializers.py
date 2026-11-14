from rest_framework import serializers
from .models import Item
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class ItemSerializer(serializers.ModelSerializer):
    user_name= UserSerializer(read_only=True)
    class Meta:
        model = Item
        fields = ["id", "user_name", "item_name", "item_description", "item_price", "upload_image"]

    def validate_item_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Item price cannot be less than 0")
        return value

    def validate(self, data):
        if data['item_name'].lower() == data['item_description'].lower():
            raise serializers.ValidationError("Item name cannot be the same as description")
        return data




