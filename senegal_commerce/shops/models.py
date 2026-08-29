from django.db import models
from django.conf import settings
from django.urls import reverse
from PIL import Image

class Shop(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name="Propriétaire"
    )
    name = models.CharField(max_length=200, verbose_name="Nom de la boutique")
    description = models.TextField(blank=True, verbose_name="Description")
    address = models.TextField(verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    logo = models.ImageField(upload_to='shop_logos/', blank=True, verbose_name="Logo")
    banner = models.ImageField(upload_to='shop_banners/', blank=True, verbose_name="Bannière")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def has_pro_badge(self):
        from subscriptions.services import user_has_pro_badge
        return user_has_pro_badge(self.owner)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Redimensionner le logo
        if self.logo:
            img = Image.open(self.logo.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.logo.path)

    class Meta:
        verbose_name = "Boutique"
        verbose_name_plural = "Boutiques"
        ordering = ['-created_at']


class Order(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_name = models.CharField(max_length=100)
    delivery_phone = models.CharField(max_length=20)
    delivery_address = models.TextField()
    delivery_city = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20, choices=[
        ('orange_money', 'Orange Money'),
        ('wave', 'Wave')
    ])
    transaction_id = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande #{self.pk} - {self.user.username}"
