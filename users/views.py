from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Q, Avg

# মডেল ইম্পোর্টস (তোমার অ্যাপ স্ট্রাকচার অনুযায়ী পাথ মিলিয়ে নিও)
from services.models import Service
from orders.models import Order
from reviews.models import Review
from .permissions import IsSeller, IsBuyer

class SellerDashboardView(APIView):
    permission_classes = [IsSeller]

    def get(self, request):
        user = request.user

        total_services = Service.objects.filter(seller=user, is_active=True).count()

        order_stats = Order.objects.filter(seller=user).aggregate(
            pending_orders=Count('id', filter=Q(status='Pending')),
            in_progress_orders=Count('id', filter=Q(status='In Progress')),
            completed_orders=Count('id', filter=Q(status='Completed')),
            total_earnings=Sum('price_at_order', filter=Q(status='Completed'))
        )

        review_stats = Review.objects.filter(seller=user).aggregate(
            average_rating=Avg('rating')
        )

        earnings = order_stats['total_earnings'] or 0.0
        rating = review_stats['average_rating'] or 0.0

        payload = {
            "total_services": total_services,
            "pending_orders": order_stats['pending_orders'],
            "in_progress_orders": order_stats['in_progress_orders'],
            "completed_orders": order_stats['completed_orders'],
            "total_earnings": float(earnings),
            "average_rating": round(float(rating), 1)
        }

        return Response(payload, status=status.HTTP_200_OK)


class BuyerDashboardView(APIView):
    permission_classes = [IsBuyer]

    def get(self, request):
        user = request.user

        buyer_stats = Order.objects.filter(buyer=user).aggregate(
            total_orders=Count('id'),
            completed_orders=Count('id', filter=Q(status='Completed')),
            cancelled_orders=Count('id', filter=Q(status='Cancelled')),
            active_orders=Count('id', filter=Q(status__in=['Pending', 'In Progress']))
        )

        payload = {
            "total_orders": buyer_stats['total_orders'],
            "completed_orders": buyer_stats['completed_orders'],
            "cancelled_orders": buyer_stats['cancelled_orders'],
            "active_orders": buyer_stats['active_orders']
        }

        return Response(payload, status=status.HTTP_200_OK)