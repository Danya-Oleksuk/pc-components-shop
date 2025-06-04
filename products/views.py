from django.views.generic import DetailView, ListView, TemplateView

from django.core.cache import cache

from .models import Category, Product


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


class ProductsListView(ListView):
    template_name = "products/products_list.html"
    model = Product
    paginate_by = 9
    ordering = ["name"]
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()

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

        return context