from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.popular_list, name='popular_list'),
    path('shop/', views.product_list, name='product_list'),
    path('shop/<slug:slug>/', views.product_detail,
         name='product_detail'),
    path('shop/category/<slug:category_slug>', views.product_list,
         name='product_list_by_category'),
]
