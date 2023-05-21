from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.

@require_POST
def cart_add(request, product_id):
    """Add Product to Cart View"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    """Remove Priduct from the Cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """Cart View"""
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True,
        })
    return render(request, 'cart/detail.html', context={'cart': cart})

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
