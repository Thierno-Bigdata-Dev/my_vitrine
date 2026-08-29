from .models import Cart

def cart_count(request):
    """
    Processeur de contexte pour injecter le nombre d'articles du panier 
    dans tous les gabarits HTML.
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.total_items
            return {
                'cart_item_count': count,
                'car_item_count': count, # support de la faute de frappe dans base.html
            }
        except Cart.DoesNotExist:
            pass
    return {
        'cart_item_count': 0,
        'car_item_count': 0,
    }
