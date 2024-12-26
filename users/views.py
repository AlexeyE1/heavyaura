from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, UserRegistrationFrom, ProfileForm
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from orders.models import Order, OrderItem


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,
                                      password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse_lazy('main:product'))
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationFrom(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success = (
                request, f'{user.username}, Successful Registration'
            )
            return HttpResponseRedirect(reverse_lazy('user:login'))
    else:
        form = UserRegistrationFrom

    return render(request, 'users/registration.html')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, isinstance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success = (request, 'Profile was changed')
            return HttpResponseRedirect(reverse_lazy('user:profile'))
    else:
        form = ProfileForm(isinstance=request.user)
    
    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            'items',
            queryset=OrderItem.objects.select_related('product')
        )
    ).order_by('-id')

    return render(request, 'users/profile.html', {'form': form,
                                                  'orders': orders})


def logout(request):
    auth.logout(request)
    return redirect(reverse_lazy('main:product_list'))