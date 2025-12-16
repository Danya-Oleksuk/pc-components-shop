from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.v2.orders.serializers import (
    OrderDisplaySerializer,
)
from orders.models.order import Order


class OrderListApi(ListAPIView):
    serializer_class = OrderDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    search_fields = ("user__username", "status", "first_name", "last_name")
