from django.db import models
from django.utils.text import slugify

from products.models.category import Category


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=600)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=500)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products_images", null=True, blank=True)
    available = models.BooleanField(default=True, db_index=True)
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications",
    )
    spec_name = models.CharField(max_length=200)
    spec_value = models.CharField(max_length=200)
    spec_value_numeric = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        verbose_name = "Product specification"
        verbose_name_plural = "Product specifications"

    def __str__(self):
        return f"{self.spec_name}: {self.spec_value}"
