"""
products/services.py
--------------------
Couche service (MVC) pour la gestion des produits.
Les vues délèguent ici toute la logique métier.
"""
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Product, Category


def get_filtered_products(query=None, category_id=None, min_price=None, max_price=None, page=1, per_page=12):
    """
    Filtre et pagine les produits actifs selon les critères donnés.
    Returns:
        (page_obj, categories) — produits paginés + liste des catégories actives
    """
    products = Product.objects.filter(is_active=True, shop__is_active=True).select_related('shop', 'category')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    paginator = Paginator(products, per_page)
    page_obj = paginator.get_page(page)

    categories = Category.objects.filter(is_active=True)

    return page_obj, categories


def get_related_products(product, limit=4):
    """
    Retourne les produits similaires (même catégorie, hors produit courant).
    """
    return Product.objects.filter(
        category=product.category,
        is_active=True,
        shop__is_active=True
    ).exclude(pk=product.pk).select_related('shop')[:limit]


def create_product(form, shop):
    """
    Sauvegarde un nouveau produit et l'associe à une boutique.
    Args:
        form: ProductForm validé (commit=False)
        shop: instance Shop
    Returns:
        instance Product sauvegardée
    """
    product = form.save(commit=False)
    product.shop = shop
    product.save()
    return product


def update_product(form):
    """
    Met à jour un produit existant via un formulaire valide.
    Returns:
        instance Product mise à jour
    """
    return form.save()


def delete_product(product):
    """
    Supprime un produit et retourne son nom pour le message de confirmation.
    Returns:
        (product_name, shop) — pour la redirection
    """
    product_name = product.name
    shop = product.shop
    product.delete()
    return product_name, shop


def get_vendor_products(user):
    """
    Retourne tous les produits appartenant aux boutiques d'un vendeur.
    """
    return Product.objects.filter(shop__owner=user).select_related('shop', 'category')
