"""
accounts/services.py
--------------------
Couche service (MVC) pour la gestion des utilisateurs.
Les vues délèguent ici toute la logique métier.
"""
from shops.models import Shop
from products.models import Product


def get_vendor_dashboard_data(user):
    """
    Retourne les données du tableau de bord vendeur.
    Args:
        user: instance CustomUser (type='vendor')
    Returns:
        dict avec shops, total_products, total_active_shops, active_sub
    """
    shops = Shop.objects.filter(owner=user).order_by('-created_at')
    total_products = Product.objects.filter(shop__owner=user).count()
    total_active_shops = shops.filter(is_active=True).count()

    from subscriptions.services import get_active_subscription
    active_sub = get_active_subscription(user)

    return {
        'shops': shops,
        'total_products': total_products,
        'total_active_shops': total_active_shops,
        'active_sub': active_sub,
    }


def get_customer_dashboard_data(user):
    """
    Retourne les données du tableau de bord client.
    Args:
        user: instance CustomUser (type='customer')
    Returns:
        dict avec cart_items_count
    """
    from customers.models import Cart
    cart_count = 0
    try:
        cart = Cart.objects.get(user=user)
        cart_count = cart.total_items
    except Cart.DoesNotExist:
        pass

    return {
        'cart_items_count': cart_count,
    }
