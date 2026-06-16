import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from core.models import Product, Box, Order, OrderItem

pytestmark = pytest.mark.django_db


def test_product_properties():
    product = Product(
        name="Test Phone", 
        length=Decimal('15.50'), 
        width=Decimal('8.00'), 
        height=Decimal('1.20'), 
        weight=Decimal('0.20')
    )
    assert product.volume == Decimal('148.80')
    assert product.sorted_dimensions == [Decimal('1.20'), Decimal('8.00'), Decimal('15.50')]
    assert str(product) == "Test Phone (15.50x8.00x1.20 cm, 0.20 kg)"


def test_product_validation():
    # Negative dimension should raise ValidationError on full_clean
    product = Product(name="Invalid Product", length=-1.00, width=5.00, height=5.00, weight=1.00)
    with pytest.raises(ValidationError):
        product.full_clean()


def test_box_properties():
    box = Box(
        name="Small Box", 
        inner_length=Decimal('20.00'), 
        inner_width=Decimal('15.00'), 
        inner_height=Decimal('10.00'), 
        max_weight=Decimal('5.00'), 
        cost=Decimal('1.50')
    )
    assert box.volume == Decimal('3000.00')
    assert box.sorted_dimensions == [Decimal('10.00'), Decimal('15.00'), Decimal('20.00')]
    assert str(box) == "Small Box (Cost: 1.50, Max Wt: 5.00 kg)"


def test_order_properties():
    order = Order.objects.create()
    p1 = Product.objects.create(name="Phone", length=15.00, width=8.00, height=1.00, weight=0.20)
    p2 = Product.objects.create(name="Book", length=20.00, width=15.00, height=3.00, weight=0.80)

    OrderItem.objects.create(order=order, product=p1, quantity=2)  # volume = 240, weight = 0.4
    OrderItem.objects.create(order=order, product=p2, quantity=1)  # volume = 900, weight = 0.8

    assert order.total_weight == Decimal('1.20')
    assert order.total_volume == Decimal('1140.00')


def test_order_item_validation():
    order = Order.objects.create()
    product = Product.objects.create(name="Item", length=5, width=5, height=5, weight=1)
    
    # Quantity 0 should fail validation
    item = OrderItem(order=order, product=product, quantity=0)
    with pytest.raises(ValidationError):
        item.full_clean()
