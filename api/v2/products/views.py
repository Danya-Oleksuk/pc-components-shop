from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

from api.v2.products.serializers import (
    CategoryCreateSerializer,
    CategoryDisplaySerializer,
    CategoryUpdateSerializer,
    ProductCreateSerializer,
    ProductDisplaySerializer,
    ProductUpdateSerializer,
)
from products.services.crud import product_delete, category_delete
from products.models.product import Product
from products.models.category import Category


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


class ProductCreateApi(GenericAPIView):
    input_serializer_class = ProductCreateSerializer
    output_serializer_class = ProductDisplaySerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        if not request.data:
            return Response(
                {"message": "No data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.input_serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        display_serializer = self.output_serializer_class(product)
        return Response(display_serializer.data, status=status.HTTP_201_CREATED)


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


class ProductDeleteApi(GenericAPIView):
    serializer_class = None
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.none()

    def get_queryset(self):
        user = self.request.user
        assert user.is_anonymous is False

        queryset = Product.objects.all()

        return queryset

    def delete(self, request: Request, pk: int) -> Response:
        product = self.get_object()
        assert self.request.user.is_anonymous is False
        product_delete(product=product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListApi(ListAPIView):
    serializer_class = CategoryDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    search_fields = ("name", "description")


class CategoryDetailApi(GenericAPIView):
    serializer_class = CategoryDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.none()

    def get(self, request: Request, pk: int) -> Response:
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"message": "Category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CategoryDisplaySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryCreateApi(GenericAPIView):
    input_serializer_class = CategoryCreateSerializer
    output_serializer_class = CategoryDisplaySerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        if not request.data:
            return Response(
                {"message": "No data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.input_serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        category = serializer.save()

        display_serializer = self.output_serializer_class(category)
        return Response(display_serializer.data, status=status.HTTP_201_CREATED)


class CategoryUpdateApi(GenericAPIView):
    input_serializer_class = CategoryUpdateSerializer
    output_serializer_class = CategoryDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()

    def get_object(self, pk: int) -> Category:
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Category.DoesNotExist("Category not found")

    def patch(self, request: Request, pk: int) -> Response:
        categories = self.get_object(pk)

        serializer = self.input_serializer_class(
            instance=categories, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        category = serializer.update(
            instance=categories, validated_data=serializer.validated_data
        )

        display_serializer = self.output_serializer_class(category)
        return Response(display_serializer.data, status=status.HTTP_200_OK)


class CategoryDeleteApi(GenericAPIView):
    serializer_class = None
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.none()

    def get_queryset(self):
        user = self.request.user
        assert user.is_anonymous is False

        queryset = Category.objects.all()

        return queryset

    def delete(self, request: Request, pk: int) -> Response:
        category = self.get_object()
        assert self.request.user.is_anonymous is False
        category_delete(category=category)
        return Response(status=status.HTTP_204_NO_CONTENT)
