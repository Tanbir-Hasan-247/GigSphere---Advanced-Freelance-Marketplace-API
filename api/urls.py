from django.urls import include, path
from rest_framework.routers import DefaultRouter
from services.views import ServiceViewSet 
from services.views import CategoryListView 
from orders.views import (
    PlaceOrderView,
    OrderListView,
    OrderStatusUpdateView,
    NotificationListView,
    NotificationReadView
)
from reviews.views import (
    CreateReviewView,
    ReviewDetailView,
    ServiceReviewsListView
)
from users.views import SellerDashboardView, BuyerDashboardView

router = DefaultRouter()
router.register("services", ServiceViewSet, basename="service")
router.register("categories", CategoryListView, basename="category") 

urlpatterns = [
    path("", include(router.urls)),
    
    path("services/<int:service_id>/order/", PlaceOrderView.as_view(), name="place-order"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/status/", OrderStatusUpdateView.as_view(), name="order-status-update"),
    
    path("notifications/", NotificationListView.as_view(), name="notification-list"),
    path("notifications/<int:pk>/read/", NotificationReadView.as_view(), name="notification-read"),

    path("orders/<int:order_id>/review/", CreateReviewView.as_view(), name="order-review-submit"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
    path("services/<int:service_id>/reviews/", ServiceReviewsListView.as_view(), name="service-reviews-list"),
    
    path("seller/dashboard/", SellerDashboardView.as_view(), name="seller-dashboard"),
    path("buyer/dashboard/", BuyerDashboardView.as_view(), name="buyer-dashboard"),

    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]