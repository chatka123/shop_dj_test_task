from django.urls import path


from . import views
from .views import CategoryAPIView, ProductAPIView, RegisterUser, LoginUser


urlpatterns = [
    path('', views.index, name='index'),
    path('category_list/', views.CategoryListView.as_view(), name='category_list'),
    path('product_list/', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:subcategory_slug>/', views.SubCategoryDetailView.as_view(), name='show_subcategory'),
    path('product/<slug:product_slug>/', views.ProductDetailView.as_view(), name='show_product'),
    path('remove_from_cart/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('remove_cart', views.DeleteCartItemsView.as_view(), name='remove_cart'),
    path('add_to_cart/<slug:product_slug>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartListView.as_view(), name='show_cart'),
    path('api/v1/category_list/', CategoryAPIView.as_view()),
    path('api/v1/product_list/', ProductAPIView.as_view()),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
]