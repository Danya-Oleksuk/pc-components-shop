from rest_framework import viewsets, permissions

from cart.models import Cart
from .serializers import CartSerializer


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Cart.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.kwargs.get("user_id")
        product_id = serializer.validated_data["product"].id

        cart = Cart.objects.filter(user_id=user_id, product_id=product_id).first()

        if cart:
            cart.quantity += 1
            cart.save()
        else:
            serializer.save(user_id=user_id)
