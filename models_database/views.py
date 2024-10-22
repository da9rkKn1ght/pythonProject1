from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from models_database.models import Product
from django_filters.views import FilterView
from models_database import filters

class ProductsList(FilterView):
    template_name = 'models_database/products_list.html'
    model = Product
    context_object_name = 'products'
    filterset_class = filters.Product

class ProductDetail(DetailView):
    template_name = 'models_database/product_detail.html'
    model = Product
    context_object_name = 'product'

class ProductsUpdate(UpdateView):
    template_name = 'models_database/product_form.html'
    model = Product
    fields = ['product_name', 'price', 'description']

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})

class ProductsDelete(DeleteView):
    template_name = 'models_database/product_confirm_delete.html'
    model = Product
    success_url = reverse_lazy('products_list')

class ProductCreate(CreateView):
    template_name = 'models_database/product_create.html'
    model = Product
    fields = ['product_name', 'description', 'price', 'quantity', 'image', 'category']
    success_url = reverse_lazy('products_list')