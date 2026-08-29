from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plan, Subscription
from .forms import PlanPaymentForm
from . import services
from accounts.permissions import is_vendor

@login_required
@is_vendor
def plan_list(request):
    """
    Affiche la liste des plans disponibles.
    """
    plans = Plan.objects.all().order_by('price')
    # S'assurer que les plans par défaut existent
    if not plans.exists():
        services.get_or_create_default_plans()
        plans = Plan.objects.all().order_by('price')
        
    active_sub = services.get_active_subscription(request.user)
    
    context = {
        'plans': plans,
        'active_sub': active_sub,
    }
    return render(request, 'subscriptions/plans.html', context)


@login_required
@is_vendor
def subscribe(request, plan_id):
    """
    Permet de souscrire à un plan, avec simulation de paiement.
    """
    plan = get_object_or_404(Plan, id=plan_id)
    active_sub = services.get_active_subscription(request.user)

    # Si l'utilisateur a déjà ce plan actif
    if active_sub and active_sub.plan == plan and not active_sub.is_expired:
        messages.info(request, f"Vous êtes déjà abonné au plan {plan.name}.")
        return redirect('dashboard')

    # Si le plan choisi est Gratuit (0 FCFA)
    if plan.price == 0:
        services.create_subscription_after_payment(
            user=request.user,
            plan=plan,
            payment_method='orange_money', # non pertinent pour gratuit
            phone_number='000000000',
            transaction_id='GRATUIT'
        )
        messages.success(request, f"Votre abonnement au plan {plan.name} a été activé.")
        return redirect('subscription_success')

    if request.method == 'POST':
        form = PlanPaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            phone_number = form.cleaned_data['phone_number']
            transaction_id = form.cleaned_data['transaction_id']

            services.create_subscription_after_payment(
                user=request.user,
                plan=plan,
                payment_method=payment_method,
                phone_number=phone_number,
                transaction_id=transaction_id
            )
            messages.success(request, f"Paiement reçu ! Votre abonnement {plan.name} est actif.")
            return redirect('subscription_success')
    else:
        form = PlanPaymentForm()

    context = {
        'plan': plan,
        'form': form,
    }
    return render(request, 'subscriptions/subscribe.html', context)


@login_required
@is_vendor
def subscription_success(request):
    """
    Page de confirmation de l'abonnement.
    """
    active_sub = services.get_active_subscription(request.user)
    return render(request, 'subscriptions/success.html', {'active_sub': active_sub})
