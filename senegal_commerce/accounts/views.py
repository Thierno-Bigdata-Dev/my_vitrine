"""
accounts/views.py
-----------------
Contrôleur (MVC) — reçoit les requêtes, délègue au service, retourne la réponse.
Aucune logique métier ici.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, UserProfileForm
from . import services


class SignUpView(CreateView):
    """Inscription d'un nouvel utilisateur."""
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Compte créé avec succès ! Vous pouvez maintenant vous connecter.')
        return response


@login_required
def profile_view(request):
    """Affichage et modification du profil utilisateur."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès !')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def dashboard_view(request):
    """Tableau de bord — redirige vers la vue adaptée au type d'utilisateur."""
    user = request.user

    if user.user_type == 'vendor':
        data = services.get_vendor_dashboard_data(user)
        return render(request, 'accounts/vendor_dashboard.html', {'user': user, **data})

    data = services.get_customer_dashboard_data(user)
    return render(request, 'accounts/customer_dashboard.html', {'user': user, **data})


def custom_logout(request):
    """Déconnexion de l'utilisateur."""
    logout(request)
    return redirect('home')
