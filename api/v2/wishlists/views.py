from rest_framework.generics import (
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated

from api.v2.wishlists.serializers import (
    WishlistDisplaySerializer,
)
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
