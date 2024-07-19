from django.urls import path
from .views import product_view, category_list, product_detail_view

app_name = 'shop'

urlpatterns = [
    path('', product_view, name='products'), 
    path('search/<slug:slug>/', category_list, name='category-list'), 
    path('<slug:slug>/', product_detail_view, name='product-detail'),
    
]