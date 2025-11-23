from rest_framework.request import Request
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.v2.products.serializers import (
    ProductDisplaySerializer,
    ProductUpdateSerializer,
)
from products.models import Product


class ProductListApi(ListAPIView):
    serializer_class = ProductDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    search_fields = ("name", "category__name")


class ProductDetailApi(GenericAPIView):
    serializer_class = ProductDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.none()

    def get(self, request: Request, pk: int) -> Response:
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ProductDisplaySerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductUpdateApi(GenericAPIView):
    input_serializer_class = ProductUpdateSerializer
    output_serializer_class = ProductDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()

    def get_object(self, pk: int) -> Product:
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Product.DoesNotExist("Product not found")

    def patch(self, request: Request, pk: int) -> Response:
        products = self.get_object(pk)

        serializer = self.input_serializer_class(
            instance=products, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        product = serializer.update(
            instance=products, validated_data=serializer.validated_data
        )

        display_serializer = self.output_serializer_class(product)

        return Response(display_serializer.data, status=status.HTTP_200_OK)
