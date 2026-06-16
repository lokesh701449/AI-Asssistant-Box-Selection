from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, BoxViewSet, OrderViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'boxes', BoxViewSet, basename='box')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
