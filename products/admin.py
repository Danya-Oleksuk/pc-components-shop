from django.contrib import admin

from products.models.product import Product, ProductSpecification
from products.models.category import Category
from products.models.wishlist import Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "available", "created_at")
    list_filter = ("category", "available")
    search_fields = ("name",)

    inlines = [ProductSpecificationInline]


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ("product", "spec_name", "spec_value", "spec_value_numeric")
    search_fields = ("spec_name",)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "added_at")
    list_filter = ("user",)
    search_fields = ("user__username", "product__name")
    ordering = ("-added_at",)
