from rest_framework import serializers
from cart.models.cart import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ("user",)
