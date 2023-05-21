from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, DetailView
from .models import Category, Product
from cart.forms import CartAddProductForm

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 16)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render (request, 'shop/product/list.html', context={
        'category': category,
        'categories': categories,
        'products': products,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', context={
        'product': product,
        'cart_product_form': cart_product_form,
    })

def filter_by_price(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    products = Product.objects.filter(price__range=(min_price, max_price))
    return render(request, 'shop/product/list.html', {'products': products})

def search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(name__icontains=query, available=True)
    else:
        results = []
    return render(request, 'shop/search.html', {'results': results, 'query': query})