from django.db import models

from cart.models import Cart


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, "Створено"),
        (PAID, "Сплачено"),
        (ON_WAY, "У дорозі"),
        (DELIVERED, "Доставлений"),
    )

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    address = models.CharField(max_length=256)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    basket_history = models.JSONField(default=dict)

    def __str__(self):
        return f"Order #{self.id}. {self.first_name} {self.last_name}"

    def update_after_payment(self):
        cart = Cart.objects.filter(user=self.user)

        total_sum = sum(item.total_price for item in cart)

        self.status = self.PAID
        self.total_price = total_sum

        self.basket_history = {
            "purchased_items": [
                {
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "total_price": float(item.total_price),
                }
                for item in cart
            ],
            "total_sum": float(total_sum),
        }
        cart.delete()
        self.save()

    class Meta:
        verbose_name_plural = "Orders"
        verbose_name = "Order"
