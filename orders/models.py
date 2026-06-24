from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_placed')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_received')
    service = models.ForeignKey('services.Service', on_delete=models.PROTECT, related_name='orders')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)  # Snapshot Pricing
    requirements_note = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.service.title} ({self.status})"


class OrderStatusLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_logs')
    old_status = models.CharField(max_length=20, default='Pending')
    new_status = models.CharField(max_length=20, default='Pending')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order.id}: {self.old_status} -> {self.new_status}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.username} - Read: {self.is_read}"