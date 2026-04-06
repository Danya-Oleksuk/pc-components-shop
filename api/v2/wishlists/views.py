from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from api.v2.wishlists.serializers import (
    WishlistDisplaySerializer,
)
from products.services.crud import wishlist_delete
from products.models.wishlist import Wishlist


class WishlistListView(ListAPIView):
    serializer_class = WishlistDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Wishlist.objects.all()
    search_fields = ("product__name",)

    def get_queryset(self):
        is_admin = self.request.user.is_staff or self.request.user.is_superuser
        if is_admin:
            return self.queryset
        return self.queryset.filter(user=self.request.user)


class WishlistDeleteView(GenericAPIView):
    serializer_class = None
    permission_classes = (IsAuthenticated,)
    queryset = Wishlist.objects.all()

    def get_object(self):
        is_admin = self.request.user.is_staff or self.request.user.is_superuser
        if not is_admin:
            self.queryset = self.queryset.filter(user=self.request.user)
        return super().get_object()

    def delete(self, request: Request, pk: int) -> Response:
        wishlist = self.get_object()
        wishlist_delete(wishlist=wishlist)
        return Response(status=status.HTTP_204_NO_CONTENT)
