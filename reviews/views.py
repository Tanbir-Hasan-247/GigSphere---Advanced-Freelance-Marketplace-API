from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsReviewOwner
from orders.models import Order

class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            context['order'] = Order.objects.get(id=self.kwargs.get('order_id'))
        except Order.DoesNotExist:
            context['order'] = None
        return context

    def perform_create(self, serializer):
        order = Order.objects.get(id=self.kwargs.get('order_id'))
        serializer.save(
            order=order,
            buyer=self.request.user,
            seller=order.seller,
            service=order.service
        )


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsReviewOwner]
    http_method_names = ['get', 'patch', 'delete']  # PUT ব্লক করা হলো স্কোপ টাইট রাখতে


class ServiceReviewsListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Review.objects.filter(service_id=self.kwargs.get('service_id')).select_related('buyer', 'seller')