"""
customers/services.py
---------------------
Couche service (MVC) pour la gestion du panier et des commandes.
Les vues délèguent ici toute la logique métier.
"""
from .models import Cart, CartItem
from products.models import Product


def get_or_create_cart(user):
    """
    Récupère ou crée le panier d'un utilisateur.
    Returns:
        (cart, created) — tuple Django standard
    """
    return Cart.objects.get_or_create(user=user)


def add_to_cart(user, product):
    """
    Ajoute un produit au panier de l'utilisateur.
    Si déjà présent, incrémente la quantité de 1.
    Returns:
        (cart, cart_item, created) — cart actuel, item, et si item vient d'être créé
    """
    cart, _ = get_or_create_cart(user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return cart, cart_item, created


def update_cart_item(cart_item, quantity):
    """
    Met à jour la quantité d'un article du panier.
    Si quantity <= 0, supprime l'article.
    Returns:
        bool — True si mis à jour, False si supprimé
    """
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        return True
    else:
        cart_item.delete()
        return False


def remove_from_cart(cart_item):
    """
    Supprime un article du panier.
    Returns:
        str — nom du produit supprimé
    """
    product_name = cart_item.product.name
    cart_item.delete()
    return product_name


def get_featured_products_for_home(limit=8):
    """
    Retourne les produits vedettes actifs pour la page d'accueil.
    """
    return Product.objects.filter(
        is_featured=True,
        is_active=True,
        shop__is_active=True
    ).select_related('shop', 'category')[:limit]
