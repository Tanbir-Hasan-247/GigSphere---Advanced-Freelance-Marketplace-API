from rest_framework import serializers
from .models import Order, Notification
from services.models import Service

class OrderSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    service_title = serializers.CharField(source='service.title', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'buyer', 'buyer_name', 'seller', 'seller_name', 
            'service', 'service_title', 'status', 'price_at_order', 
            'requirements_note', 'created_at', 'completed_at'
        ]
        read_only_fields = ['buyer', 'seller', 'service', 'status', 'price_at_order', 'created_at', 'completed_at']


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        current_status = self.instance.status
        allowed_statuses = dict(Order.STATUS_CHOICES)
        
        if value not in allowed_statuses:
            raise serializers.ValidationError("Invalid status name.")

        if current_status == value:
            return value

        if current_status in ['Completed', 'Cancelled']:
            raise serializers.ValidationError(f"Cannot change status of a {current_status} order.")

        if value == 'In Progress' and current_status != 'Pending':
            raise serializers.ValidationError("Order can only move to 'In Progress' from 'Pending'.")
            
        if value == 'Completed' and current_status != 'In Progress':
            raise serializers.ValidationError("Order can only be marked 'Completed' from 'In Progress'.")

        return value


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'message', 'created_at']