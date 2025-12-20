from rest_framework import serializers
from api.mixins import ReadOnlySerializerMixin, CreateOnlySerializerMixin

from users.models.users import User
from orders.models.order import Order
from orders.services.crud import (
    order_create,
    order_update,
)


class OrderDisplaySerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "total_price",
            "status",
            "city",
            "warehouse",
            "basket_history",
            "purchased_items",
            "notes",
            "created_at",
            "updated_at",
        )


class OrderCreateSerializer(CreateOnlySerializerMixin, serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
    )
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    city = serializers.CharField(max_length=100)
    warehouse = serializers.CharField(max_length=100)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    phone = serializers.CharField(max_length=20)
    notes = serializers.CharField(allow_blank=True, required=False)

    def validate(self, attrs):
        request = self.context.get("request")
        assert request is not None, "Request is required"
        user = request.user

        if not user.is_staff and attrs.get("user") is not None:
            raise serializers.ValidationError(
                {
                    "permission": "You do not have permission "
                    "to create an order for another user."
                }
            )

        if user.is_staff and "user" not in attrs:
            attrs["user"] = user

        if attrs.get("total_price", 0) < 0:
            raise serializers.ValidationError(
                {"total_price": "Total price must be a non-negative value."}
            )

        if not attrs.get("first_name") or not attrs.get("last_name"):
            raise serializers.ValidationError(
                {"credentials": "First name and last name cannot be empty."}
            )

        if not attrs.get("city") or not attrs.get("warehouse"):
            raise serializers.ValidationError(
                {"location": "City and warehouse cannot be empty."}
            )

        if not attrs.get("phone"):
            raise serializers.ValidationError(
                {"phone": "Phone number cannot be empty."}
            )

        if len(attrs.get("phone")) < 10:
            raise serializers.ValidationError(
                {"phone": "Phone number must contain at least 10 digits."}
            )

        return attrs

    def create(self, validated_data):
        return order_create(**validated_data)


class OrderUpdateSerializer(CreateOnlySerializerMixin, serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
    )
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    city = serializers.CharField(max_length=100, required=False)
    warehouse = serializers.CharField(max_length=100, required=False)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )
    phone = serializers.CharField(max_length=20, required=False)
    notes = serializers.CharField(allow_blank=True, required=False)

    def validate(self, attrs):
        request = self.context.get("request")
        assert request is not None, "Request is required"
        user = request.user

        if not user.is_staff and attrs.get("user") is not None:
            raise serializers.ValidationError(
                {
                    "permission": "You do not have permission "
                    "to create an order for another user."
                }
            )

        if user.is_staff and "user" not in attrs:
            attrs["user"] = user

        return attrs

    def update(self, instance, validated_data):
        return order_update(order=instance, **validated_data)
