"""
customers/views.py
------------------
Contrôleur (MVC) — reçoit les requêtes, délègue au service, retourne la réponse.
Aucune logique métier ici.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from products.models import Product
from .models import Cart, CartItem
from . import services


def home(request):
    """Page d'accueil — affiche les produits vedettes."""
    featured_products = services.get_featured_products_for_home()
    return render(request, 'customers/home.html', {'featured_products': featured_products})


@login_required
def add_to_cart(request, product_id):
    """Ajouter un produit au panier (supporte AJAX)."""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart, cart_item, created = services.add_to_cart(request.user, product)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.name} ajouté au panier',
            'cart_count': cart.total_items,
        })

    messages.success(request, f'{product.name} ajouté au panier')
    return redirect('product_detail', pk=product_id)


@login_required
def cart_view(request):
    """Afficher le contenu du panier."""
    cart, _ = services.get_or_create_cart(request.user)
    return render(request, 'customers/cart.html', {'cart': cart})


@login_required
def update_cart_item(request, item_id):
    """Mettre à jour la quantité d'un article du panier."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        services.update_cart_item(cart_item, quantity)

    return redirect('cart_view')


@login_required
def remove_from_cart(request, item_id):
    """Supprimer un article du panier."""
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    product_name = services.remove_from_cart(cart_item)
    messages.success(request, f"'{product_name}' supprimé du panier")
    return redirect('cart_view')


@login_required
def checkout(request):
    """Page de validation du panier."""
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'customers/checkout.html', {'cart': cart})
