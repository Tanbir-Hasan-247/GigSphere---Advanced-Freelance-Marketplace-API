from django.contrib import admin
from .models import Order, OrderStatusLog, Notification

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderStatusLog)
admin.site.register(Notification)
