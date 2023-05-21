from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.shortcuts import render, get_object_or_404

# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, template_name='orders/order/created.html', context={'order': order})
    else:
        form = OrderCreateForm()
    if not request.user.is_authenticated:
        return render(request, 'shop/auth.html')
    
    return render(request, template_name='orders/order/create.html', 
                    context={
                        'form': form,
                        'cart': cart
                    }
            )
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders\order\order_detail.html', {'order': order})