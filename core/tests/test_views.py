import pytest
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Product, Box, Order, OrderItem

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


def test_product_crud(client):
    # Create product
    payload = {
        "name": "Widget",
        "length": "10.00",
        "width": "5.50",
        "height": "2.00",
        "weight": "0.50"
    }
    response = client.post("/api/products/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Widget"
    assert float(response.data["volume"]) == 110.00

    # List products
    response = client.get("/api/products/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


def test_box_crud(client):
    # Create box
    payload = {
        "name": "Box A",
        "inner_length": "20.00",
        "inner_width": "20.00",
        "inner_height": "20.00",
        "max_weight": "10.00",
        "cost": "2.50"
    }
    response = client.post("/api/boxes/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Box A"

    # List boxes
    response = client.get("/api/boxes/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


def test_order_nested_creation_and_update(client):
    product = Product.objects.create(name="Gizmo", length=5, width=5, height=5, weight=1)
    
    # Create order with items
    payload = {
        "items": [
            {
                "product": product.id,
                "quantity": 3
            }
        ]
    }
    response = client.post("/api/orders/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    order_id = response.data["id"]
    assert len(response.data["items"]) == 1
    assert response.data["items"][0]["product"] == product.id
    assert response.data["items"][0]["quantity"] == 3
    assert float(response.data["total_weight"]) == 3.00
    assert float(response.data["total_volume"]) == 375.00

    # Update order items
    update_payload = {
        "items": [
            {
                "product": product.id,
                "quantity": 5
            }
        ]
    }
    response = client.put(f"/api/orders/{order_id}/", update_payload, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["items"][0]["quantity"] == 5
    assert float(response.data["total_weight"]) == 5.00
    assert float(response.data["total_volume"]) == 625.00


def test_recommend_box_endpoint(client):
    # Setup Products and Boxes
    p = Product.objects.create(name="Mini Toy", length=5, width=5, height=5, weight=0.2)
    b1 = Box.objects.create(name="Tiny Box", inner_length=6, inner_width=6, inner_height=6, max_weight=1, cost=1.00)
    b2 = Box.objects.create(name="Large Box", inner_length=15, inner_width=15, inner_height=15, max_weight=5, cost=3.00)

    # Order that fits in Tiny Box
    order1 = Order.objects.create()
    OrderItem.objects.create(order=order1, product=p, quantity=1)

    # Recommend box for Order 1
    response = client.get(f"/api/orders/{order1.id}/recommend-box/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["recommended_box"]["id"] == b1.id
    assert response.data["recommended_box"]["name"] == "Tiny Box"

    # Order that exceeds Tiny Box weight / volume limits
    order2 = Order.objects.create()
    OrderItem.objects.create(order=order2, product=p, quantity=10) # volume = 125 * 10 = 1250 cm³, exceeding Tiny Box volume (216 cm³)

    # Recommend box for Order 2
    response = client.get(f"/api/orders/{order2.id}/recommend-box/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["recommended_box"]["id"] == b2.id
    assert response.data["recommended_box"]["name"] == "Large Box"

    # Order that is way too large/heavy for any box
    order3 = Order.objects.create()
    huge_p = Product.objects.create(name="Huge Object", length=50, width=50, height=50, weight=100)
    OrderItem.objects.create(order=order3, product=huge_p, quantity=1)

    # Recommend box for Order 3
    response = client.get(f"/api/orders/{order3.id}/recommend-box/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["recommended_box"] is None
    assert "No suitable box found" in response.data["message"]
