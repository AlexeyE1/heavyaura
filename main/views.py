from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.forms import CartAddProductForm


def popular_list(request):
    products = Product.objects.filter(available=True)[:3]
    return render(request, 'main/index/index.html',
                  {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product,
                                slug=slug,
                                available=True)
    form = CartAddProductForm
    return render(request, 'main/product/detail.html',
                  {'product': product,
                   'form': form})


def product_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Фильтрация по категории
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Пагинация
    paginator = Paginator(products, 10)
    try:
        current_page = paginator.page(int(page))
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    
    return render(request, 'main/product/list.html', {
        'category': category,
        'categories': categories,
        'products': current_page,
    })