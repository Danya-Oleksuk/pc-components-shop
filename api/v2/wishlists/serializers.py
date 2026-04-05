from rest_framework import serializers
from api.mixins import (
    ReadOnlySerializerMixin,
    CreateOnlySerializerMixin,
    UpdateOnlySerializerMixin,
)
from api.v2.products.serializers import ProductDisplaySerializer
from api.v2.users.serializers import UserDisplaySerializer
from products.models import Wishlist


class WishlistDisplaySerializer(
    ReadOnlySerializerMixin, serializers.ModelSerializer
):
    product = ProductDisplaySerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = (
            "id",
            "user",
            "product",
            "added_at",
        )

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if not request:
            return fields
        
        is_admin = (
            request.user.is_staff
            or request.user.is_superuser
        )
        if not is_admin:
            fields.pop("user", None)
        return fields