from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductProxy


def product_view(request):
    products = ProductProxy.objects.all()
    return render(request, 'shop/product.html', {'products': products})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'shop/category_list.html', context)

def product_detail_view(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})






