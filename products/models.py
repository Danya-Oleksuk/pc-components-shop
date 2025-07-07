from django.db import models
from django.utils.text import slugify

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(max_length=600)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=500)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products_images")
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "Product"
        ordering = ["-created_at"]


class ProductSpecification(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    spec_name = models.CharField(max_length=200)
    spec_value = models.CharField(max_length=200)
    spec_value_numeric = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"{self.spec_name}: {self.spec_value}"

    class Meta:
        verbose_name_plural = "Product specifications"
        verbose_name = "Product specification"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"
        verbose_name = "Wishlist"
        ordering = ["-added_at"]
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username}: {self.product.name}"