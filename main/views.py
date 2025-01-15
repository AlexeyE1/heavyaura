from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.forms import CartAddProductForm
from django.views.generic import ListView, DetailView


class PopularListView(ListView):
    model = Product
    template_name = 'main/index/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(available=True)[:3]


# def popular_list(request):
#     products = Product.objects.filter(available=True)[:3]
#     return render(request, 'main/index/index.html',
#                   {'products': products})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product/detail.html'
    form = CartAddProductForm
    context_object_name = 'product'

    def get_object(self, queryset = None):
        return get_object_or_404(Product, slug=self.kwargs[self.slug_url_kwarg], available=True)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

# def product_detail(request, slug):
#     product = get_object_or_404(Product,
#                                 slug=slug,
#                                 available=True)
#     form = CartAddProductForm
#     return render(request, 'main/product/detail.html',
#                   {'product': product,
#                    'form': form})


class ProductListView(ListView):
    model = Product
    template_name = 'main/product/list.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        products = Product.objects.filter(available=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        return products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            context['category'] = category
        context['categories'] = Category.objects.all()
        return context

# def product_list(request, category_slug=None):
#     page = request.GET.get('page', 1)
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
    
#     # Фильтрация по категории
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
    
#     # Пагинация
#     paginator = Paginator(products, 10)
#     try:
#         current_page = paginator.page(int(page))
#     except EmptyPage:
#         current_page = paginator.page(paginator.num_pages)
    
#     return render(request, 'main/product/list.html', {
#         'category': category,
#         'categories': categories,
#         'products': current_page,
#     })