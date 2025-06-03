from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Category
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, **kwargs):
    cache.delete('products_list')

@receiver([post_save, post_delete], sender=Category)
def clear_product_cache(sender, **kwargs):
    cache.delete('category_list')