from django.db import models
from django.conf import settings
from django.utils import timezone

class Plan(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du plan")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix (FCFA)")
    max_shops = models.PositiveIntegerField(verbose_name="Nombre max de boutiques")
    max_products_per_shop = models.PositiveIntegerField(verbose_name="Nombre max de produits par boutique")
    has_badge = models.BooleanField(default=False, verbose_name="Badge de mise en avant")
    has_analytics = models.BooleanField(default=False, verbose_name="Accès aux statistiques")
    description = models.TextField(verbose_name="Description")
    duration_days = models.PositiveIntegerField(default=30, verbose_name="Durée (jours)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price} FCFA"

    class Meta:
        verbose_name = "Plan tarifaire"
        verbose_name_plural = "Plans tarifaires"
        ordering = ['price']


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="subscriptions",
        verbose_name="Utilisateur"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, verbose_name="Plan")
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Date de début")
    end_date = models.DateTimeField(verbose_name="Date de fin")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} (jusqu'au {self.end_date.strftime('%d/%m/%Y')})"

    @property
    def is_expired(self):
        return timezone.now() > self.end_date

    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
        ordering = ['-start_date']


class PlanPayment(models.Model):
    PAYMENT_METHODS = [
        ('orange_money', 'Orange Money'),
        ('wave', 'Wave'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="plan_payments",
        verbose_name="Utilisateur"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, verbose_name="Plan")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name="Méthode de paiement")
    phone_number = models.CharField(max_length=20, verbose_name="Numéro Mobile Money")
    transaction_id = models.CharField(max_length=100, verbose_name="ID de transaction")
    is_approved = models.BooleanField(default=True, verbose_name="Approuvé")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de transaction")

    def __str__(self):
        return f"Paiement {self.amount} FCFA - {self.user.username} ({self.get_payment_method_display()})"

    class Meta:
        verbose_name = "Paiement de plan"
        verbose_name_plural = "Paiements de plans"
        ordering = ['-created_at']
