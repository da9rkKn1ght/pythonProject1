from rest_framework import serializers
from models_database import models
from models_database.models import Category


class User(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = models.User
        fields = '__all__'

    def get_username(self, obj):
        return obj.username.upper()

class UserProfile(serializers.ModelSerializer):
    user = User(read_only=True)
    user_id = serializers.IntegerField(required=False, allow_null=True)
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = '__all__'

    def get_phone_number(self, obj):
        return obj.phone_number

class Category(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class Product(serializers.ModelSerializer):
    category = Category(read_only=True)
    category_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.SerializerMethodField()
    class Meta:
        model = models.Product
        fields = '__all__'

    def get_quantity(self, obj):
        if models.Product.objects.filter(product_name=obj.product_name).exists():
            return obj.quantity
        return None


class OrderItem(serializers.ModelSerializer):
    product = Product(read_only=True)
    product_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    price = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = models.OrderItem
        fields = '__all__'

    def get_price(self, obj):
        return obj.price if obj.price is not None else 0

    def get_quantity(self, obj):
        return obj.quantity if obj.quantity > 0 else None


class Order(serializers.ModelSerializer):
    user = User(read_only=True)
    user_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    items = OrderItem(source='orderitem', many=True)
    total_price = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    class Meta:
        model = models.Order
        fields = '__all__'

    def get_total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.orderitem.all())

    def get_status(self, obj):
        return obj.status if obj.status else "Неизвестен"