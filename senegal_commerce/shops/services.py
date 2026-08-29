"""
shops/services.py
-----------------
Couche service (MVC) pour la gestion des boutiques.
Les vues délèguent ici toute la logique métier.
"""
from django.db.models import Q

from .models import Shop
from products.models import Product


def get_filtered_shops(query=None, city=None):
    """
    Filtre les boutiques actives selon les critères donnés.
    Returns:
        (shops_qs, cities_list) — boutiques filtrées + liste des villes disponibles
    """
    shops = Shop.objects.filter(is_active=True).order_by('-created_at')

    if query:
        shops = shops.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if city:
        shops = shops.filter(city__icontains=city)

    cities = Shop.objects.filter(is_active=True).values_list('city', flat=True).distinct()

    return shops, cities


def get_shop_products(shop, limit=8):
    """
    Retourne les produits actifs d'une boutique.
    """
    return Product.objects.filter(shop=shop, is_active=True).select_related('category')[:limit]


def create_shop(form, owner):
    """
    Crée une nouvelle boutique et l'associe à son propriétaire.
    Args:
        form: ShopForm validé (commit=False)
        owner: instance CustomUser
    Returns:
        instance Shop sauvegardée
    """
    shop = form.save(commit=False)
    shop.owner = owner
    shop.save()
    return shop


def update_shop(form):
    """
    Met à jour une boutique existante via un formulaire valide.
    Returns:
        instance Shop mise à jour
    """
    return form.save()


def get_vendor_shops(user):
    """
    Retourne toutes les boutiques d'un vendeur.
    """
    return Shop.objects.filter(owner=user).order_by('-created_at')
