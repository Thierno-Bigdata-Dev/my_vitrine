from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Client'),
        ('vendor', 'Vendeur'),
    ]
    
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='customer',
        verbose_name="Type d'utilisateur"
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name="Téléphone"
    )
    address = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Adresse"
    )
    city = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Ville"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"