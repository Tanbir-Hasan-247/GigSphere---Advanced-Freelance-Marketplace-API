from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    SELLER = "Seller"
    BUYER = "Buyer"
    USER_TYPE_CHOICES = [
        (SELLER, "Seller"),
        (BUYER, "Buyer")
    ]

    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    role = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.email}'s Seller Profile"
    
class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="buyer_profile")
    bio = models.TextField(blank=True)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.email}'s Buyer Profile"