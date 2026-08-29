from django.contrib import admin
from .models import Shop

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'city', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'city', 'created_at']
    search_fields = ['name', 'owner__username', 'city', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'description', 'owner', 'is_active')
        }),
        ('Contact', {
            'fields': ('address', 'city', 'phone', 'email')
        }),
        ('Images', {
            'fields': ('logo', 'banner')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
