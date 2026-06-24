from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.db import models

from .models import Order, Notification
from .serializers import OrderSerializer, OrderStatusUpdateSerializer, NotificationSerializer
from .permissions import IsOrderParticipant, IsNotificationOwner
from services.models import Service
from users.models import User


class PlaceOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        service_id = self.kwargs.get('service_id')
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"detail": "Service not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role != User.BUYER:
            return Response({"detail": "Only buyers can place orders."}, status=status.HTTP_403_FORBIDDEN)

        if service.seller == request.user:
            return Response({"detail": "You cannot purchase your own service."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order = serializer.save(
            buyer=request.user,
            seller=service.seller,
            service=service,
            price_at_order=service.price
        )
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'seller':
            return Order.objects.filter(seller=user).select_related('buyer', 'seller', 'service')
        return Order.objects.filter(buyer=user).select_related('buyer', 'seller', 'service')


class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrderParticipant]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('status')
        user = request.user

        if new_status in ['In Progress', 'Completed'] and user != instance.seller:
            return Response(
                {"detail": "Only the seller can progress or complete this order."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        if new_status == 'Completed':
            instance.completed_at = timezone.now()

        serializer.save()
        return Response(OrderSerializer(instance).data, status=status.HTTP_200_OK)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class NotificationReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotificationOwner]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = True
        instance.save()
        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)