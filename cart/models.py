from django.db import models

from products.models.product import Product
from users.models.users import User


class CartStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    ORDERED = "ordered", "Ordered"
    CANCELLED = "cancelled", "Cancelled"


class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="in_carts",
    )
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=CartStatus.choices,
        default=CartStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name_plural = "Carts"
        verbose_name = "Cart"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.email}: {self.product.name} x{self.quantity}"
