from decimal import Decimal
from typing import Any

from django.db import transaction

from pc_components_shop.services.crud import model_update
from products.models.category import Category
from products.models.product import Product


@transaction.atomic
def product_create(
    *,
    name: str,
    category: str | None = None,
    price: Decimal = Decimal("0.00"),
    description: str = "",
    available: bool = True,
    image: Any = None,
) -> Product:
    product = Product.objects.create(
        name=name,
        category=category,
        price=price,
        description=description,
        available=available,
        image=image,
    )

    product.full_clean()
    product.save()
    product.refresh_from_db()
    return product


def product_update(
    *,
    product: Product,
    **fields: Any,
) -> Product:
    product, updates = model_update(model=product, **fields)
    return product


def product_delete(
    *,
    product: Product,
) -> None:
    product.delete()


def category_create(
    *,
    name: str,
    description: str = "",
) -> Category:
    category = Category.objects.create(
        name=name,
        description=description,
    )

    category.full_clean()
    category.save()
    category.refresh_from_db()
    return category


def category_update(
    *,
    category: Category,
    **fields: Any,
) -> Category:
    category, updates = model_update(model=category, **fields)
    return category


def category_delete(
    *,
    category: Category,
) -> None:
    category.delete()
