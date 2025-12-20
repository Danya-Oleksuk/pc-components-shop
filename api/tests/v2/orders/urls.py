from django.urls import reverse


def get_order_create_url():
    return reverse("v2:orders:order-create")


def get_order_update_url(pk):
    return reverse("v2:orders:order-update", kwargs={"pk": pk})


def get_order_delete_url(pk):
    return reverse("v2:orders:order-delete", kwargs={"pk": pk})
