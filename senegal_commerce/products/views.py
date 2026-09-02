"""
products/views.py
-----------------
Contrôleur (MVC) — reçoit les requêtes, délègue au service, retourne la réponse.
Aucune logique métier ici.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.permissions import is_vendor
from shops.models import Shop
from .models import Product
from .forms import ProductForm
from . import services


def product_list(request):
    """Liste de tous les produits actifs avec filtrage et pagination."""
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    page = request.GET.get('page', 1)

    products, categories = services.get_filtered_products(
        query=query,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        page=page,
    )

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    """Détail d'un produit avec produits similaires."""
    product = get_object_or_404(Product, pk=pk, is_active=True, shop__is_active=True)
    related_products = services.get_related_products(product)

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
@is_vendor
def create_product(request, shop_id):
    """Créer un nouveau produit dans une boutique (vendeurs seulement)."""
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)

    from subscriptions.services import can_add_product
    if not can_add_product(request.user, shop):
        messages.warning(request, "Vous avez atteint la limite de produits autorisés par boutique pour votre abonnement actuel. Veuillez mettre à niveau votre plan pour ajouter d'autres produits.")
        return redirect('plan_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = services.create_product(form, shop)
            messages.success(request, f"Produit '{product.name}' ajouté avec succès.")
            return redirect('shop_detail', pk=shop.id)
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form, 'shop': shop})


@login_required
def edit_product(request, pk):
    """Modifier un produit existant (propriétaire seulement)."""
    product = get_object_or_404(Product, id=pk, shop__owner=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            services.update_product(form)
            messages.success(request, "Produit modifié avec succès.")
            return redirect('shop_detail', pk=product.shop.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, pk):
    """Supprimer un produit (propriétaire seulement)."""
    product = get_object_or_404(Product, id=pk, shop__owner=request.user)

    if request.method == 'POST':
        product_name, shop = services.delete_product(product)
        messages.success(request, f"Produit '{product_name}' supprimé avec succès.")
        return redirect('shop_detail', pk=shop.pk)

    return render(request, 'products/confirm_delete.html', {'product': product})


@login_required
def my_products(request):
    """Liste des produits du vendeur connecté."""
    if request.user.user_type != 'vendor':
        messages.error(request, "Page réservée aux vendeurs.")
        return redirect('dashboard')

    products = services.get_vendor_products(request.user)
    return render(request, 'products/my_products.html', {'products': products})