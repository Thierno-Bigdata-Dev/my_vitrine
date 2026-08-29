from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'phone', 'city', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active', 'city']
    search_fields = ['username', 'email', 'phone']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('user_type', 'phone', 'address', 'city')}),
    )