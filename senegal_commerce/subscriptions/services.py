from django.utils import timezone
from datetime import timedelta
from .models import Plan, Subscription, PlanPayment
from shops.models import Shop
from products.models import Product

def get_or_create_default_plans():
    """
    Crée les trois plans de base s'ils n'existent pas encore.
    """
    plans_data = [
        {
            'name': 'Gratuit',
            'price': 0,
            'max_shops': 1,
            'max_products_per_shop': 5,
            'has_badge': False,
            'has_analytics': False,
            'description': 'Formule de base pour démarrer votre activité en ligne au Sénégal. Permet de tester la plateforme.',
            'duration_days': 30
        },
        {
            'name': 'Standard',
            'price': 5000,
            'max_shops': 2,
            'max_products_per_shop': 20,
            'has_badge': False,
            'has_analytics': True,
            'description': 'Idéal pour les commerces en croissance. Permet de gérer deux boutiques et d\'avoir accès aux statistiques.',
            'duration_days': 30
        },
        {
            'name': 'Professionnel',
            'price': 15000,
            'max_shops': 100, # Pratiquement illimité
            'max_products_per_shop': 1000, # Pratiquement illimité
            'has_badge': True,
            'has_analytics': True,
            'description': 'Pour les professionnels du commerce. Illimité en boutiques et produits avec un badge exclusif "Pro" pour booster vos ventes.',
            'duration_days': 30
        }
    ]
    
    created_plans = []
    for p_data in plans_data:
        plan, created = Plan.objects.get_or_create(
            name=p_data['name'],
            defaults=p_data
        )
        created_plans.append(plan)
    return created_plans


def get_active_subscription(user):
    """
    Récupère l'abonnement actif d'un utilisateur.
    Si aucun abonnement actif n'existe, en crée un par défaut avec le plan 'Gratuit'.
    """
    if not user.is_authenticated:
        return None

    # Assurons-nous que les plans par défaut existent
    get_or_create_default_plans()

    # Recherche d'un abonnement actif non expiré
    now = timezone.now()
    active_sub = Subscription.objects.filter(
        user=user,
        is_active=True,
        end_date__gt=now
    ).first()

    if active_sub:
        return active_sub

    # Si aucun actif, on recherche le plan gratuit
    free_plan = Plan.objects.filter(name='Gratuit').first()
    if not free_plan:
        free_plan = Plan.objects.create(
            name='Gratuit',
            price=0,
            max_shops=1,
            max_products_per_shop=5,
            has_badge=False,
            has_analytics=False,
            description='Formule de base gratuite.',
            duration_days=3650  # 10 ans pour le gratuit par défaut
        )

    # Création d'un abonnement gratuit par défaut
    start = timezone.now()
    end = start + timedelta(days=free_plan.duration_days)
    
    # Désactiver les anciens abonnements s'il y en a
    Subscription.objects.filter(user=user, is_active=True).update(is_active=False)

    default_sub = Subscription.objects.create(
        user=user,
        plan=free_plan,
        start_date=start,
        end_date=end,
        is_active=True
    )
    return default_sub


def can_create_shop(user):
    """
    Vérifie si le vendeur peut créer une nouvelle boutique selon les limites de son plan.
    """
    if user.user_type != 'vendor':
        return False

    sub = get_active_subscription(user)
    if not sub:
        return False

    shop_count = Shop.objects.filter(owner=user, is_active=True).count()
    return shop_count < sub.plan.max_shops


def can_add_product(user, shop):
    """
    Vérifie si le vendeur peut ajouter un produit dans une boutique donnée.
    """
    # Vérifier que l'utilisateur possède bien la boutique
    if shop.owner != user:
        return False

    sub = get_active_subscription(user)
    if not sub:
        return False

    product_count = Product.objects.filter(shop=shop, is_active=True).count()
    return product_count < sub.plan.max_products_per_shop


def create_subscription_after_payment(user, plan, payment_method, phone_number, transaction_id):
    """
    Enregistre le paiement et active le nouvel abonnement.
    """
    # 1. Enregistrer le paiement
    payment = PlanPayment.objects.create(
        user=user,
        plan=plan,
        amount=plan.price,
        payment_method=payment_method,
        phone_number=phone_number,
        transaction_id=transaction_id,
        is_approved=True
    )

    # 2. Désactiver les abonnements actifs existants
    Subscription.objects.filter(user=user, is_active=True).update(is_active=False)

    # 3. Créer le nouvel abonnement
    start = timezone.now()
    end = start + timedelta(days=plan.duration_days)
    
    subscription = Subscription.objects.create(
        user=user,
        plan=plan,
        start_date=start,
        end_date=end,
        is_active=True
    )

    return subscription, payment


def user_has_pro_badge(user):
    """
    Retourne True si l'utilisateur possède un plan avec le badge Pro actif.
    """
    if not user or not user.is_authenticated:
        return False
    
    sub = get_active_subscription(user)
    return sub.plan.has_badge if sub else False
