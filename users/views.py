from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .forms import UserLoginForm, UserRegistrationFrom, ProfileForm
from orders.models import Order, OrderItem
from django.db.models import Prefetch


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main:product_list')


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationFrom
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        auth.login(self.request, user)
        messages.success(self.request, f'{user.username}, Successful Registration')
        return redirect(self.get_success_url())
    

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProfileForm(instance=self.request.user)

        # Заказы пользователя
        context['orders'] = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product')
            )
        ).order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was changed')
            return redirect(reverse_lazy('user:profile'))
        else:
            # Если форма невалидна, передаем её в контекст
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)