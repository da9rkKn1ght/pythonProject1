from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from models_database.models import Product, User, Category, UserProfile, Order, OrderItem
from django_filters.views import FilterView
from models_database import filters
from rest_framework import viewsets
from rest_framework.response import Response
from models_database import serializers

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


class UserAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.User


class UserProfilesAPI(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = serializers.UserProfile


class CategoryAPI(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.Category


class ProductAPI(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.Product

class OrderAPI(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = serializers.Order

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = serializer.save(user=request.user)  # При необходимости связываем с пользователем

        order.total_price = sum(item.price * item.quantity for item in order.orderitem_set.all())
        order.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class OrderItemAPI(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItem

    def perform_create(self, serializer):
        order_item = serializer.save()
        order = order_item.order
        order.total_price = sum(item.price * item.quantity for item in order.orderitem_set.all())
        order.save()