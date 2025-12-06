from django.db import models

from products.models.product import Product
from users.models.users import User


class Wishlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by",
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"
        ordering = ("-added_at",)
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "user",
                    "product",
                ),
                name="unique_user_product_wishlist",
            )
        ]

    def __str__(self):
        return f"{self.user.username}: {self.product.name}"
