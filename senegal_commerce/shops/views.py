"""
shops/views.py
--------------
Contrôleur (MVC) — reçoit les requêtes, délègue au service, retourne la réponse.
Aucune logique métier ici.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.permissions import is_vendor
from .models import Shop
from .forms import ShopForm
from . import services


@login_required
def shop_list(request):
    """Liste de toutes les boutiques actives avec filtrage."""
    query = request.GET.get('q')
    city = request.GET.get('city')

    shops, cities = services.get_filtered_shops(query=query, city=city)

    context = {
        'shops': shops,
        'cities': cities,
        'query': query,
        'selected_city': city,
    }
    return render(request, 'shops/shop_list.html', context)


@login_required
def shop_detail(request, pk):
    """Détail d'une boutique avec ses produits actifs."""
    shop = get_object_or_404(Shop, pk=pk, is_active=True)
    products = services.get_shop_products(shop)

    context = {
        'shop': shop,
        'products': products,
    }
    return render(request, 'shops/shop_detail.html', context)


@login_required
@is_vendor
def create_shop(request):
    """Créer une nouvelle boutique (vendeurs seulement)."""
    from subscriptions.services import can_create_shop
    if not can_create_shop(request.user):
        messages.warning(request, "Vous avez atteint le nombre maximum de boutiques autorisées par votre abonnement actuel. Veuillez mettre à niveau votre plan pour en créer de nouvelles.")
        return redirect('plan_list')

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = services.create_shop(form, owner=request.user)
            messages.success(request, f"Boutique '{shop.name}' créée avec succès !")
            return redirect('shop_detail', pk=shop.pk)
    else:
        form = ShopForm()

    return render(request, 'shops/create_shop.html', {'form': form})


@login_required
def edit_shop(request, pk):
    """Modifier une boutique (propriétaire seulement)."""
    shop = get_object_or_404(Shop, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            services.update_shop(form)
            messages.success(request, f"Boutique '{shop.name}' modifiée avec succès !")
            return redirect('shop_detail', pk=shop.pk)
    else:
        form = ShopForm(instance=shop)

    return render(request, 'shops/edit_shop.html', {'form': form, 'shop': shop})


@login_required
@is_vendor
def my_shops(request):
    """Liste des boutiques du vendeur connecté."""
    shops = services.get_vendor_shops(request.user)
    return render(request, 'shops/my_shops.html', {'shops': shops})


@login_required
def access_denied(request):
    """Page d'accès refusé."""
    return render(request, 'common/access_denied.html')
