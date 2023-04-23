from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .forms import ItemsCartForm, ConfirmForm
from .serializers import CategorySerializer, ProductSerializer
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from .utils import PaginatedListViewMixin

from .models import Category, SubCategory, Product, Cart, CartItem


def index(request):
    return render(request, 'goods/index.html')


class CategoryListView(PaginatedListViewMixin, ListView):
    model = Category
    template_name = 'goods/category_list.html'
    context_object_name = 'categories'


class ProductListView(PaginatedListViewMixin, ListView):
    model = Product
    template_name = 'goods/product_list.html'
    context_object_name = 'products'


class SubCategoryDetailView(DetailView):
    model = SubCategory
    template_name = 'goods/subcategory.html'
    context_object_name = 'subcategory'
    slug_url_kwarg = 'subcategory_slug'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'goods/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'


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


class CartListView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'goods/show_cart.html'
    context_object_name = 'items'

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        queryset = CartItem.objects.filter(cart=cart)
        print(queryset, '!!!!!!!!!!!1')
        return queryset

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        print(context)
        context['cart'] = Cart.objects.get(user=self.request.user)
        return context


class RemoveFromCartView(LoginRequiredMixin, FormView):
    form_class = ItemsCartForm
    template_name = 'goods/remove_from_cart.html'
    success_url = reverse_lazy('show_cart')

    def form_valid(self, form):
        item = get_object_or_404(CartItem, pk=self.kwargs['item_id'])
        quantity_for_del = form.cleaned_data.get('quantity')
        if item.quantity > quantity_for_del:
            item.quantity -= quantity_for_del
            item.save()
        else:
            item.delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs.get('item_id')
        context['item'] = get_object_or_404(CartItem, id=item_id)
        return context


class DeleteCartItemsView(FormView):
    form_class = ConfirmForm
    template_name = 'goods/confirm_cart_del.html'
    success_url = reverse_lazy('show_cart')

    def form_valid(self, form):
        # Получаем все объекты CartItem, относящиеся к текущему пользователю
        cart_items = CartItem.objects.filter(cart__user=self.request.user)

        # Удаляем все объекты
        cart_items.delete()

        return super().form_valid(form)


class AddToCartView(LoginRequiredMixin, FormView):
    form_class = ItemsCartForm
    template_name = 'goods/add_to_cart.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        quantity = form.cleaned_data['quantity']
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        context['product'] = product

        referer_url = self.request.META.get('HTTP_REFERER')
        if referer_url:
            self.request.session['referer_url'] = referer_url

        return context

    def get_success_url(self):
        # Получаем url, с которого пришел пользователь
        url = self.request.session.get('referer_url')
        if url:
            return url
        return self.success_url


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'goods/register.html'
    success_url = reverse_lazy('/')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'goods/login.html/'

    def get_success_url(self):
        return '/'


def logout_user(request):
    logout(request)
    return redirect('index')
