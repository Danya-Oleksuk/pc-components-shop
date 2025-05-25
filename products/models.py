from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products_images/')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "Product"
        ordering = ['-created_at']

class ProductSpecification(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    spec_name = models.CharField(max_length=200)
    spec_value = models.CharField(max_length=200)
    spec_value_numeric = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.spec_name}: {self.spec_value}"

    class Meta:
        verbose_name_plural = "Product specifications"
        verbose_name = "Product specification"