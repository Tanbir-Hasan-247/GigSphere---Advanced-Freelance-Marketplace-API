from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'order', 'buyer', 'buyer_name', 'seller', 'seller_name', 
            'service', 'rating', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['buyer', 'seller', 'service', 'order']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method == 'POST':
            order = self.context.get('order')
            
            if not order:
                raise serializers.ValidationError({"detail": "Associated order not found."})

            if order.status != 'Completed':
                raise serializers.ValidationError({"status": "You can only review an order after it is 'Completed'."})
            
            if order.buyer != request.user:
                raise serializers.ValidationError({"detail": "You are not authorized to review this order."})
            
            if Review.objects.filter(order=order).exists():
                raise serializers.ValidationError({"detail": "You have already submitted a review for this order."})

        return attrs