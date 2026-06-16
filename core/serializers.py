from rest_framework import serializers
from django.db import transaction
from .models import Product, Box, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    volume = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'length', 'width', 'height', 'weight', 'volume']


class BoxSerializer(serializers.ModelSerializer):
    volume = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Box
        fields = ['id', 'name', 'inner_length', 'inner_width', 'inner_height', 'max_weight', 'cost', 'volume']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    total_weight = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_volume = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'total_weight', 'total_volume']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_weight = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_volume = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'items', 'total_weight', 'total_volume']

    def validate_items(self, value):
        """
        Validate that the order has at least one item.
        """
        if not value:
            raise serializers.ValidationError("An order must have at least one item.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item_data in items_data:
                OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            
            if items_data is not None:
                # Clear existing items and recreate
                instance.items.all().delete()
                for item_data in items_data:
                    OrderItem.objects.create(order=instance, **item_data)
                    
        return instance
