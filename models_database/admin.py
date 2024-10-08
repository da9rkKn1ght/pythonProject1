from django.contrib import admin
from models_database import models
# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone_number')

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description')

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'image')

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('total_price', 'status')

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'price')