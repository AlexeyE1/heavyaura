from django.urls import path
from .views import *


app_name = 'main'

urlpatterns = [
    path('',
         PopularListView.as_view(),
         name='popular_list'),
    path('shop/',
         ProductListView.as_view(),
         name='product_list'),
    path('shop/<slug:slug>/',
         ProductDetailView.as_view(),
         name='product_detail'),
    path('shop/category/<slug:category_slug>',
          ProductListView.as_view(),
          name='product_list_by_category'),
]
