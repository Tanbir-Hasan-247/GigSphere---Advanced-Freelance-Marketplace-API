from django.shortcuts import render
from rest_framework.permissions import AllowAny
from services import filters
from services.filters import ServiceFilter
from services.serializers import CategorySerializer, ServiceSerializer
from .models import Category, Service
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .permissions import IsSellerRole, IsServiceOwner
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.

class CategoryListView(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsSellerRole, IsServiceOwner]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'delivery_days']
    ordering = ['-created_at'] 

    def get_queryset(self):
        return Service.objects.filter(is_active=True).select_related('seller', 'category')

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Soft Delete override"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(
            {"detail": "Service has been deactivated successfully."}, 
            status=status.HTTP_204_NO_CONTENT
        )