from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import custom_logout

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', custom_logout, name='logout'),
]