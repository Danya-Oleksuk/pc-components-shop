from django.db import models
from django.db import transaction
from cart.models import Cart


class OrderStatus(models.TextChoices):
    CREATED = 0, "Створено"
    PAID = 1, "Сплачено"
    ON_WAY = 2, "У дорозі"
    DELIVERED = 3, "Доставлений"


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    warehouse = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    basket_history = models.JSONField(default=dict)
    purchased_items = models.TextField(default="")
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Orders"
        verbose_name = "Order"
        ordering = ("-created_at",)

    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_paid(self):
        return self.status >= OrderStatus.PAID

    @property
    def is_delivered(self):
        return self.status == OrderStatus.DELIVERED

    def update_after_payment(self):
        cart = Cart.objects.filter(user=self.user).select_related("product")
        total_sum = sum(item.total_price for item in cart)

        self.status = OrderStatus.PAID
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
        self.purchased_items = "\n".join(
            [f"{item.product.name} - {item.quantity} шт." for item in cart]
        )

        with transaction.atomic():
            self.save()
            cart.delete()

    def cancel(self):
        if self.is_paid:
            raise ValueError("Cannot cancel a paid order.")
        self.delete()
