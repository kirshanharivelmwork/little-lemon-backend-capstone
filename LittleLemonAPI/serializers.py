from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "title"]

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "featured", "category", "category_id"]

class CartSerializer(serializers.ModelSerializer):
    menuitem_title = serializers.CharField(source="menuitem.title", read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = ["id", "menuitem", "menuitem_title", "quantity", "unit_price", "price"]
        read_only_fields = ["unit_price"]

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem_title = serializers.CharField(source="menuitem.title", read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ["id", "menuitem", "menuitem_title", "quantity", "unit_price", "price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = Order
        fields = ["id", "user", "username", "delivery_crew", "status", "total", "date", "items"]
        read_only_fields = ["user", "total", "date", "items"]
