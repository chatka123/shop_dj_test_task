from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .serializers import CategorySerializer, ProductSerializer

from .models import Category, SubCategory, Product


def index(request):
    return render(request, 'goods/index.html')


def category_list(request):
    category_list = Category.objects.all()
    paginator = Paginator(category_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'goods/category_list.html', context={'categories': page_obj})


def product_list(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'goods/product_list.html', context={'products': page_obj})


class CategoryListPagination(PageNumberPagination):
    page_size = 10


class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryListPagination


class ProductPagination(PageNumberPagination):
    page_size = 10


class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

