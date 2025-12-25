from rest_framework import serializers
from api.mixins import (
    ReadOnlySerializerMixin,
    CreateOnlySerializerMixin,
    UpdateOnlySerializerMixin,
)
from products.services.crud import (
    product_create,
    product_update,
    category_create,
    category_update,
)

from products.models.product import Product
from products.models.category import Category


class ProductDisplaySerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "price",
            "available",
            "created_at",
            "category",
        )


class ProductCreateSerializer(CreateOnlySerializerMixin, serializers.Serializer):
    name = serializers.CharField(max_length=255)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    available = serializers.BooleanField()
    image = serializers.ImageField(required=False)

    def validate(self, attrs):
        request = self.context.get("request")
        assert request is not None, "Request is required"
        user = request.user

        if not user.is_staff:
            raise serializers.ValidationError(
                {"permission": "You do not have permission to create a product."}
            )

        if attrs.get("price", 0) < 0:
            raise serializers.ValidationError(
                {"price": "Price must be a non-negative value."}
            )

        if not attrs.get("name"):
            raise serializers.ValidationError({"name": "Product name cannot be empty."})

        return attrs

    def create(self, validated_data):
        return product_create(**validated_data)


class ProductUpdateSerializer(UpdateOnlySerializerMixin, serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False
    )
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    available = serializers.BooleanField(required=False)
    image = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        return product_update(product=instance, **validated_data)


class CategoryDisplaySerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "description",
        )


class CategoryCreateSerializer(CreateOnlySerializerMixin, serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False)

    def create(self, validated_data):
        return category_create(**validated_data)


class CategoryUpdateSerializer(UpdateOnlySerializerMixin, serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        return category_update(category=instance, **validated_data)
