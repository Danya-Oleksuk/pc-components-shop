from django.views.generic import TemplateView

from .models import Product


class MainPageView(TemplateView):
    template_name = 'products/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        random_products = Product.objects.order_by('?')[:3]
        context['random_products'] = random_products

        return context