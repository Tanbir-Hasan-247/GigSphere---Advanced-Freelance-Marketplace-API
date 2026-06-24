from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review
from users.models import SellerProfile

@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def recalculate_seller_rating(sender, instance, **kwargs):
    seller = instance.seller
    stats = Review.objects.filter(seller=seller).aggregate(Avg('rating'))
    avg_rating = stats['rating__avg'] or 0.0
    
    try:
        profile = SellerProfile.objects.get(user=seller)
        profile.average_rating = round(avg_rating, 1)
        profile.save(update_fields=['average_rating'])
    except SellerProfile.DoesNotExist:
        pass