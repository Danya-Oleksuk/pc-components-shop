from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView

from products.models.product import Product
from products.models.category import Category
from products.models.wishlist import Wishlist


class MainPageView(TemplateView):
    template_name = "products/main_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        random_products = cache.get("random_products")
        if not random_products:
            random_products = Product.objects.order_by("?")[:3]
            cache.set("random_products", random_products, timeout=30)
        context["random_products"] = random_products

        return context


class ProductDetailView(DetailView):
    template_name = "products/detail.html"
    model = Product
    slug_field = "slug"
    slug_url_kwarg = "product_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        params = self.request.GET.copy()
        source = params.pop("from", [""])[0]

        if source == "main_page":
            base_url = "/"
        elif source == "catalog":
            base_url = "/products/"
        elif source == "cart":
            base_url = "/user/cart/"
        elif source == "wishlist":
            base_url = "/user/wishlist/"
        else:
            base_url = "/"

        if params:
            query_string = urlencode(params, doseq=True)
            context["back_url"] = f"{base_url}?{query_string}"
        else:
            context["back_url"] = base_url

        product = self.object

        if not product.available:
            context["not_available"] = True
            return context

        context["specs"] = product.specifications.all()

        if self.request.user.is_authenticated:
            wishlist_products = Wishlist.objects.filter(
                user=self.request.user
            ).values_list("product", flat=True)
            context["wishlist_products"] = wishlist_products

        return context


class ProductsListView(ListView):
    template_name = "products/products_list.html"
    model = Product
    paginate_by = 9
    ordering = ["name"]
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset().filter(available=True)

        category = self.request.GET.get("category")
        search = self.request.GET.get("search")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if category:
            queryset = queryset.filter(category__name=category)
        if search:
            queryset = queryset.filter(name__icontains=search)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = cache.get("category_list")
        if not categories:
            categories = Category.objects.all()
            cache.set("category_list", categories)
        context["categories"] = categories

        if self.request.user.is_authenticated:
            wishlist_products = Wishlist.objects.filter(
                user=self.request.user
            ).values_list("product", flat=True)
            context["wishlist_products"] = wishlist_products

        return context


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect(request.META.get("HTTP_REFERER", "catalog"))


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect(request.META.get("HTTP_REFERER", "catalog"))
