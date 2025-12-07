from django.contrib import admin

from orders.models.order import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("__str__", "status")
    fields = (
        "id",
        "created_at",
        ("first_name", "last_name"),
        ("city", "warehouse"),
        ("user", "phone"),
        "status",
        ("basket_history", "purchased_items"),
    )
    readonly_fields = ("id", "created_at", "basket_history", "purchased_items")
