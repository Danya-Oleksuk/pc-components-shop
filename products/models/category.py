from django.db import models


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
