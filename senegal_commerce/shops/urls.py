from django.urls import path
from . import views
from .views import access_denied

urlpatterns = [
    path('', views.shop_list, name='shop_list'),
    path('<int:pk>/', views.shop_detail, name='shop_detail'),
    path('create/', views.create_shop, name='create_shop'),
    path('<int:pk>/edit/', views.edit_shop, name='edit_shop'),
    path('my-shops/', views.my_shops, name='my_shops'),
path('access-denied/', access_denied, name='access_denied'),
]
