from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from orders.models import Order
from users.forms import UserProfileEditForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'shop/list.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():   
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration\\register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration\\register.html', {'user_form': user_form})

def user_profile(request, username):
    user_orders = Order.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'orders': user_orders,
    }
    return render(request, 'profile.html', context)

def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:user_profile', {'user': request.user})  # Перенаправлення на сторінку профілю після збереження
    else:
        form = UserProfileEditForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'edit_profile.html', context)
