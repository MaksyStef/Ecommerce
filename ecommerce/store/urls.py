from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    path('search/<str:wanted>/', views.SearchView.as_view(), name='search'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('products/<slug:product_type>/', views.CertainProductsView.as_view(), name='certain'),
    path('product/<slug:slug>/', views.ProductView.as_view(), name='product'),
    path('cart/', login_required(views.CartView.as_view()), name='cart'),
    path('favourite/', login_required(views.FavouriteView.as_view()), name='favourite'),
    path('newsletters/', views.NewslettersView.as_view(), name='newsletter'),
    path('success/', views.success_view, name='success'),
    path('failure/', views.failure_view, name='failure'),
]
