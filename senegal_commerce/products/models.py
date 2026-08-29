from django.db import models
from django.urls import reverse
from shops.models import Shop
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name="Image")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Boutique")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Catégorie")
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix (FCFA)")
    image = models.ImageField(upload_to='products/', verbose_name="Image principale")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Quantité en stock")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_featured = models.BooleanField(default=False, verbose_name="Produit vedette")
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Poids (kg)")
    dimensions = models.CharField(max_length=100, blank=True, verbose_name="Dimensions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.shop.name}"

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    @property
    def has_pro_badge(self):
        from subscriptions.services import user_has_pro_badge
        return user_has_pro_badge(self.shop.owner)

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Redimensionner l'image
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Redimensionner l'image
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)

    class Meta:
        verbose_name = "Image produit"
        verbose_name_plural = "Images produit"
