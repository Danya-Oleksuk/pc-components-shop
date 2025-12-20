from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from api.v2.orders.serializers import (
    OrderCreateSerializer,
    OrderDisplaySerializer,
    OrderUpdateSerializer,
)
from orders.services.crud import order_delete
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


class OrderUpdateApi(GenericAPIView):
    input_serializer_class = OrderUpdateSerializer
    output_serializer_class = OrderDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()

    def get_object(self, pk: int) -> Order:
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Order.DoesNotExist("Order not found")

    def patch(self, request, pk: int):
        order = self.get_object(pk)

        serializer = self.input_serializer_class(
            instance=order,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        order = serializer.update(
            instance=order, validated_data=serializer.validated_data
        )

        display_serializer = self.output_serializer_class(order)
        return Response(display_serializer.data, status=status.HTTP_200_OK)


class OrderDeleteApi(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()

    def delete(self, request, pk: int):
        order = self.get_object()
        assert self.request.user.is_anonymous is False

        order_delete(order=order)
        return Response(status=status.HTTP_204_NO_CONTENT)
