from django.contrib import admin

from .models import Category, Product, ProductSpecification

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "available", "created_at")
    list_filter = ('category', 'available')
    search_fields = ("name",)

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'spec_name', 'spec_value', 'spec_value_numeric')
    search_fields = ('spec_name',)