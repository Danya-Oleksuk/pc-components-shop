from h11 import Request
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from api.v2.products.serializers import ProductDisplaySerializer
from products.models import Product


class ProductListApi(ListAPIView):
    serializer_class = ProductDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    search_fields = ("name", "category__name")


class ProductDetailApi(APIView):
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
