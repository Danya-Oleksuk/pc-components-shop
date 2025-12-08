from django.contrib import admin

from cart.models.cart import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity")
    list_filter = ("created_at",)
