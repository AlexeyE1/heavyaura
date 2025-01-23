from django.urls import path
from .views import UserLoginView, UserRegistrationView, UserProfileView
from django.contrib.auth.views import LogoutView

app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='user:login'), name="logout"),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]