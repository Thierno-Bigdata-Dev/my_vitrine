from django.contrib import admin
from .models import Plan, Subscription, PlanPayment

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'max_shops', 'max_products_per_shop', 'has_badge', 'duration_days')
    list_filter = ('has_badge', 'has_analytics')
    search_fields = ('name', 'description')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('plan', 'is_active', 'start_date', 'end_date')
    search_fields = ('user__username', 'plan__name')

@admin.register(PlanPayment)
class PlanPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount', 'payment_method', 'phone_number', 'transaction_id', 'is_approved', 'created_at')
    list_filter = ('payment_method', 'is_approved', 'created_at')
    search_fields = ('user__username', 'transaction_id', 'phone_number')
