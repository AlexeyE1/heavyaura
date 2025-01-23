from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.views.generic.edit import FormView


class OrderCreateView(FormView):
    template_name = 'order/create.html'
    form_class = OrderCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save()
        for item in cart:
            discounted_price = item['product'].sell_price()
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=discounted_price,
                                     quantity=item['quantity'])
        cart.clear()
        self.request.session['order_id'] = order.id
        return redirect(reverse('payment:process'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context
