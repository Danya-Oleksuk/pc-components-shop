from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from products.models.product import Product
from products.models.category import Category


@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, **kwargs):
    cache.delete("products_list")


@receiver([post_save, post_delete], sender=Category)
def clear_category_cache(sender, **kwargs):
    cache.delete("category_list")
