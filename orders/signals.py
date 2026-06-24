from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Order, OrderStatusLog, Notification

@receiver(post_save, sender=Order)
def notify_new_order(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.seller,
            order=instance,
            message=f"New order received for '{instance.service.title}' from {instance.buyer.email}."
        )

        Notification.objects.create(
            recipient=instance.buyer,
            order=instance,
            message=f"Your order for '{instance.service.title}' has been placed successfully."
        )

@receiver(pre_save, sender=Order)
def track_order_status_changes(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_order = Order.objects.get(pk=instance.pk)
        if old_order.status != instance.status:
            OrderStatusLog.objects.create(
                order=instance,
                old_status=old_order.status,
                new_status=instance.status,
                changed_by=instance.seller if instance.status in ['In Progress', 'Completed'] else instance.buyer
            )

            if instance.status == 'In Progress':
                Notification.objects.create(
                    recipient=instance.buyer,
                    order=instance,
                    message=f"Your order for '{instance.service.title}' is now In Progress."
                )
            elif instance.status == 'Completed':
                Notification.objects.create(
                    recipient=instance.buyer,
                    order=instance,
                    message=f"Order completed! Please leave a review for '{instance.service.title}'."
                )
            elif instance.status == 'Cancelled':
                recipient = instance.buyer if old_order.status == 'Pending' else instance.seller
                Notification.objects.create(
                    recipient=recipient,
                    order=instance,
                    message=f"Order #{instance.id} has been cancelled."
                )
    except Order.DoesNotExist:
        pass
