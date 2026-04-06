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
    WishlistCreateSerializer,
    WishlistUpdateSerializer,
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


class WishlistCreateView(GenericAPIView):
    input_serializer_class = WishlistCreateSerializer
    output_serializer_class = WishlistDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Wishlist.objects.all()

    def post(self, request: Request) -> Response:
        serializer = self.input_serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        wishlist = serializer.save()

        display_serializer = self.output_serializer_class(wishlist)
        return Response(display_serializer.data, status=status.HTTP_201_CREATED)


class WishlistUpdateView(GenericAPIView):
    input_serializer_class = WishlistUpdateSerializer
    output_serializer_class = WishlistDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Wishlist.objects.all()

    def get_object(self):
        is_admin = self.request.user.is_staff or self.request.user.is_superuser
        if not is_admin:
            self.queryset = self.queryset.filter(user=self.request.user)
        return super().get_object()

    def patch(self, request: Request, pk: int) -> Response:
        wishlist = self.get_object()
        serializer = self.input_serializer_class(wishlist, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_wishlist = serializer.save()

        display_serializer = self.output_serializer_class(updated_wishlist)
        return Response(display_serializer.data, status=status.HTTP_200_OK)


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
