"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
     path('', views.index, name='index'),
     path('about',views.about,name='about'),
     path('cart',views.cart, name='cart'),
     path('checkout',views.checkout, name='checkout'),
     path('contact',views.contact, name='contact'),
     path('gallery',views.gallery, name='gallery'),
     path('my_account',views.my_account, name='my_account'),
     path('search',views.search, name='search'),
     path('shop_detail/<int:id>',views.shop_detail, name='shop_detail'),
     path('add_to_cart/<int:id>',views.add_to_cart, name='add_to_cart'),
     path('plus/<int:id>',views.plus, name='plus'),
     path('minus/<int:id>',views.minus, name='minus'),
     path('remove/<int:id>',views.remove, name='remove'),
     path('shop',views.shop, name='shop'),
     path('category/<int:id>',views.category,name='category'),
     path('wishlist',views.wishlist, name='wishlist'),
     path('add_to_wishlist/<int:id>',views.add_to_wishlist, name='add_to_wishlist'),
     path('wishlist_remove/<int:id>',views.wishlist_remove, name='wishlist_remove'),
     path('register',views.register, name='register'),
     path('login',views.login,name='login'),
     path('logout',views.logout,name='logout'),
     path('forget_password',views.forget_password,name='forget_password'),
     path('confirm_password',views.confirm_password,name='confirm_password'),
     path('billing_address',views.billing_address, name='billing_address'),
     path('change_address',views.change_address,name='change_address'),
     path('order',views.order,name='order'),
     path('error',views.error,name='error'),
     path('my_address',views.my_address,name='my_address'),
     path('category_gallery',views.category_gallery, name='category_gallery'),
    #  path('category_product',views.category_product, name='category_product'),
]       