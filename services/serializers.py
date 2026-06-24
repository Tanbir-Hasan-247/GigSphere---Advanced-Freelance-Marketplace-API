from rest_framework import serializers
from .models import Category, Service


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'seller', 'seller_name', 'category', 'category_name', 
            'title', 'description', 'price', 'delivery_days', 
            'requirements', 'thumbnail', 'thumbnail_url', 'is_active', 'created_at'
        ]
        read_only_fields = ['seller', 'is_active', 'created_at']

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            return request.build_absolute_uri(obj.thumbnail.url) if request else obj.thumbnail.url
        return None