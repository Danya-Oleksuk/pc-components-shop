from django.views.generic import TemplateView, ListView, DetailView

from .models import Product, Category


class MainPageView(TemplateView):
    template_name = 'products/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        random_products = Product.objects.order_by('?')[:3]
        context['random_products'] = random_products

        return context

class ProductDetailView(DetailView):
    template_name = 'products/detail.html'
    model = Product

class ProductsListView(ListView):
    template_name = 'products/products_list.html'
    model = Product
    paginate_by = 9
    ordering = ['name']
    context_object_name = 'products'


    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')

        if category:
            queryset = queryset.filter(category__slug=category)
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()
        return context
