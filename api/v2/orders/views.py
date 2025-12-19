from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from api.v2.orders.serializers import (
    OrderCreateSerializer,
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


class OrderCreateApi(GenericAPIView):
    input_serializer_class = OrderCreateSerializer
    output_serializer_class = OrderDisplaySerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if not request.data:
            return Response(
                {"message": "No data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.input_serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        display_serializer = self.output_serializer_class(order)
        return Response(display_serializer.data, status=status.HTTP_201_CREATED)
