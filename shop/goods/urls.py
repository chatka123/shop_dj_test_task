from django.urls import path


from . import views
from .views import CategoryAPIView, ProductAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('category_list/', views.category_list, name='category_list'),
    path('product_list/', views.product_list, name='product_list'),
    path('api/v1/category_list/', CategoryAPIView.as_view()),
    path('api/v1/product_list/', ProductAPIView.as_view()),
]