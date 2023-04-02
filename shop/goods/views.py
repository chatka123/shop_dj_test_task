from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Category, SubCategory


def index(request):
    return render(request, 'goods/index.html')


def category_list(request):
    category_list = Category.objects.all()
    paginator = Paginator(category_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'goods/category_list.html', context={'categories': page_obj})
