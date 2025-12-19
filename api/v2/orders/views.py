from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from api.v2.orders.serializers import (
    OrderDisplaySerializer,
)
from orders.models.order import Order


class OrderListApi(ListAPIView):
    serializer_class = OrderDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    search_fields = ("user__username", "status", "first_name", "last_name")


class OrderDetailApi(GenericAPIView):
    serializer_class = OrderDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()

    def get(self, request, pk: int):
        order = self.get_object()
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
