from django.db import models

from users.models import User
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user.email}: {self.product.name} x{self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name_plural = "Carts"
        verbose_name = "Cart"
        ordering = ['-created_at']