from django.urls import reverse


def get_product_create_url():
    return reverse("v2:products:product-create")


def get_product_update_url(pk):
    return reverse("v2:products:product-update", kwargs={"pk": pk})


def get_product_delete_url(pk):
    return reverse("v2:products:product-delete", kwargs={"pk": pk})
