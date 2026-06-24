from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):
    seller = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='services'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='services'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_days = models.PositiveIntegerField()
    requirements = models.TextField(help_text="What the seller needs to start the work")
    thumbnail = models.ImageField(upload_to='services/thumbnails/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.seller.username})"