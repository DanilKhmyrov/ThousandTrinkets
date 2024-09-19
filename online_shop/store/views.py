from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.db.models import Q

from .models import Product, Category, MainCategory


def ajax_search(request):
    query = request.GET.get('query', '')
    results_per_page = 10
    page = int(request.GET.get('page', 1))

    matching_products = Product.objects.filter(
        name__icontains=query) | Product.objects.filter(article_number__icontains=query)

    total_results = matching_products.count()
    has_more = total_results > page * results_per_page

    products = matching_products[(
        page-1)*results_per_page:page*results_per_page]

    results = [{
        'name': product.name,
        'article_number': product.article_number,
        'price': product.price,
        'category': product.category.name if product.category else '',
        'category_url': product.category.get_absolute_url() if product.category else '',
        'image_url': product.image.url if product.image else 'https://via.placeholder.com/40',
        'url': product.get_absolute_url()
    } for product in products]

    return JsonResponse({
        'results': results,
        'has_more': has_more,
        'total_results': total_results
    })


class SearchResultsView(ListView):
    model = Product
    template_name = 'store/search_results.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) | Q(article_number__icontains=query)
            )
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')
        context['query'] = query
        # Подсчитываем общее количество результатов
        if query:
            total_results = Product.objects.filter(
                Q(name__icontains=query) | Q(article_number__icontains=query)
            ).count()
        else:
            total_results = 0
        context['total_results'] = total_results
        return context


class IndexListView(ListView):
    model = Product
    template_name = 'store/index.html'
    paginate_by = 28
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.select_related('category', 'category__main_category').all()


class MainCategoryListView(ListView):
    model = MainCategory
    template_name = 'store/choose_category.html'
    context_object_name = 'main_categories'
    pk_url_kwarg = 'main_category_slug'

    def get_queryset(self):
        # Получаем все категории, принадлежащие данной главной категории
        return MainCategory.objects.prefetch_related('categories').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_main_category'] = get_object_or_404(
            MainCategory, slug=self.kwargs['main_category_slug'])
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'store/categorydetail.html'
    context_object_name = 'products'
    pk_url_kwarg = 'category_slug'
    paginate_by = 28

    def get_queryset(self):
        self.category = get_object_or_404(
            Category.objects.select_related('main_category'),
            slug=self.kwargs['category_slug']
        )
        return self.category.products.all().select_related('category', 'category__main_category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        context['current_main_category'] = self.category.main_category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    slug_field = 'article_number'
    slug_url_kwarg = 'article_number'

    def get_queryset(self):
        return Product.objects.select_related('category', 'category__main_category').filter(
            article_number=self.kwargs['article_number']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.object.category
        context['current_main_category'] = self.object.category.main_category
        return context
