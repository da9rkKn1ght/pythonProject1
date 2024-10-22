"""
URL configuration for online_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from models_database import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products_list/', views.ProductsList.as_view(), name='products_list'),
    path('product_create/', views.ProductCreate.as_view(), name='product_create'),
    path('product/<int:pk>/detail/', views.ProductDetail.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', views.ProductsUpdate.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductsDelete.as_view(), name='product_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)