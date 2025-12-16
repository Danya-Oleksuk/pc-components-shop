from rest_framework import serializers
from api.mixins import (
    ReadOnlySerializerMixin,
)

from orders.models.order import Order


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
            "basket_history",
            "purchased_items",
            "notes",
            "created_at",
            "updated_at",
        )
