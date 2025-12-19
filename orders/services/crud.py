from decimal import Decimal
from typing import Any

from django.db import transaction

from orders.models.order import Order


@transaction.atomic
def order_create(
    *,
    user: Any = None,
    first_name: str,
    last_name: str,
    city: str,
    warehouse: str,
    total_price: Decimal = Decimal("0.00"),
    phone: str,
    notes: str = "",
) -> Order:
    order = Order.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        city=city,
        warehouse=warehouse,
        total_price=total_price,
        phone=phone,
        notes=notes,
    )

    order.full_clean()
    order.save()
    order.refresh_from_db()
    return order
