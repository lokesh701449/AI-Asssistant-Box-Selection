import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from core.models import Product, Box, Order, OrderItem
from services.box_selector import BoxSelectorService

pytestmark = pytest.mark.django_db


@pytest.fixture
def sample_boxes():
    # Small Box: cost 1.50, volume 3000 (20x15x10), max_weight 5
    b1 = Box.objects.create(name="Small Box", inner_length=20.00, inner_width=15.00, inner_height=10.00, max_weight=5.00, cost=1.50)
    # Medium Box: cost 3.00, volume 12000 (30x20x20), max_weight 15
    b2 = Box.objects.create(name="Medium Box", inner_length=30.00, inner_width=20.00, inner_height=20.00, max_weight=15.00, cost=3.00)
    # Flat Box: cost 1.50, volume 2000 (40x25x2), max_weight 5 (same cost as small box, but flat and different volume)
    b3 = Box.objects.create(name="Flat Box", inner_length=40.00, inner_width=25.00, inner_height=2.00, max_weight=5.00, cost=1.50)
    # Heavy Duty Box: cost 5.00, volume 27000 (30x30x30), max_weight 50
    b4 = Box.objects.create(name="Heavy Duty Box", inner_length=30.00, inner_width=30.00, inner_height=30.00, max_weight=50.00, cost=5.00)
    return b1, b2, b3, b4


def test_recommendation_basic_fit(sample_boxes):
    small_box, medium_box, flat_box, heavy_duty_box = sample_boxes
    
    # Create order with a small product
    order = Order.objects.create()
    product = Product.objects.create(name="Phone", length=15.00, width=8.00, height=1.00, weight=0.20)
    OrderItem.objects.create(order=order, product=product, quantity=1)

    recommended = BoxSelectorService.select_box(order)
    # Flat box and Small box both fit.
    # Flat box: volume = 40 * 25 * 2 = 2000 cm³
    # Small box: volume = 20 * 15 * 10 = 3000 cm³
    # Cost for both is 1.50. Tie-breaker: smallest volume, which is flat box (2000 < 3000)
    assert recommended == flat_box


def test_recommendation_requires_larger_box_due_to_weight(sample_boxes):
    small_box, medium_box, flat_box, heavy_duty_box = sample_boxes

    # Create order with heavy but small products
    order = Order.objects.create()
    product = Product.objects.create(name="Gold Bar", length=10.00, width=5.00, height=2.00, weight=10.00)
    OrderItem.objects.create(order=order, product=product, quantity=1)

    recommended = BoxSelectorService.select_box(order)
    # Gold bar fits in flat/small box by volume/dimensions, but weight (10kg) exceeds small/flat box limit (5kg)
    # Hence it must go to Medium Box (max_weight 15kg, cost 3.00)
    assert recommended == medium_box


def test_recommendation_requires_larger_box_due_to_dimensions(sample_boxes):
    small_box, medium_box, flat_box, heavy_duty_box = sample_boxes

    # Create order with a product that is too tall for Flat Box (2cm max height)
    # Product is 5x5x5 cm, weight 0.5kg
    # Fits in Small box (10cm height limit), but not Flat box (2cm height limit)
    order = Order.objects.create()
    product = Product.objects.create(name="Rubik Cube", length=5.00, width=5.00, height=5.00, weight=0.50)
    OrderItem.objects.create(order=order, product=product, quantity=1)

    recommended = BoxSelectorService.select_box(order)
    assert recommended == small_box


def test_recommendation_rotation_handling(sample_boxes):
    small_box, medium_box, flat_box, heavy_duty_box = sample_boxes

    # Product is 2x25x40 cm (fits flat box if rotated)
    order = Order.objects.create()
    product = Product.objects.create(name="Laptop", length=2.00, width=25.00, height=40.00, weight=2.00)
    OrderItem.objects.create(order=order, product=product, quantity=1)

    recommended = BoxSelectorService.select_box(order)
    assert recommended == flat_box


def test_recommendation_no_box_fits(sample_boxes):
    # Order has a item that is too heavy even for Heavy Duty Box (50kg limit)
    order = Order.objects.create()
    product = Product.objects.create(name="Anvil", length=20.00, width=20.00, height=20.00, weight=60.00)
    OrderItem.objects.create(order=order, product=product, quantity=1)

    recommended = BoxSelectorService.select_box(order)
    assert recommended is None


def test_recommendation_empty_order(sample_boxes):
    order = Order.objects.create()
    recommended = BoxSelectorService.select_box(order)
    assert recommended is None


def test_recommendation_invalid_quantity(sample_boxes):
    from unittest.mock import MagicMock, PropertyMock, patch
    order = Order.objects.create()
    product = Product.objects.create(name="Book", length=20, width=15, height=3, weight=0.8)
    
    # Create a mock OrderItem with quantity 0
    mock_item = MagicMock(spec=OrderItem)
    mock_item.product = product
    mock_item.quantity = 0
    
    # Mock the items descriptor on the Order class
    with patch.object(Order, 'items', new_callable=PropertyMock) as mock_items:
        mock_items.return_value.all.return_value = [mock_item]
        
        with pytest.raises(ValidationError):
            BoxSelectorService.select_box(order)
