from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.plan_list, name='plan_list'),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('success/', views.subscription_success, name='subscription_success'),
]
