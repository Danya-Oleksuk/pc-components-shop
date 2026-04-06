from rest_framework import serializers
from api.mixins import ReadOnlySerializerMixin, UpdateOnlySerializerMixin
from products.services.crud import wishlist_create, wishlist_update
from api.v2.products.serializers import ProductDisplaySerializer
from products.models import Product, Wishlist


class WishlistDisplaySerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
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

        is_admin = request.user.is_staff or request.user.is_superuser
        if not is_admin:
            fields.pop("user", None)
        return fields


class WishlistCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True,
    )

    def create(self, validated_data):
        request = self.context.get("request")
        assert request is not None, "Request is required"
        assert not request.user.is_anonymous, "Authentication is required"
        user = request.user
        return wishlist_create(user=user, **validated_data)


class WishlistUpdateSerializer(UpdateOnlySerializerMixin, serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True,
    )

    def update(self, instance, validated_data):
        return wishlist_update(wishlist=instance, **validated_data)
