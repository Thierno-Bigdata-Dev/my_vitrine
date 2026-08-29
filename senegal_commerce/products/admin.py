from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop', 'category', 'price', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_featured', 'category', 'shop', 'created_at']
    search_fields = ['name', 'shop__name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'shop', 'category', 'description', 'is_active', 'is_featured')
        }),
        ('Prix et stock', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Caractéristiques', {
            'fields': ('weight', 'dimensions')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'is_main', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['product__name', 'alt_text']
