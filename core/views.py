from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Box, Order
from .serializers import ProductSerializer, BoxSerializer, OrderSerializer
from services.box_selector import BoxSelectorService



class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing products.
    """
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer


class BoxViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing packaging boxes.
    """
    queryset = Box.objects.all().order_by('cost')
    serializer_class = BoxSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing orders.
    """
    queryset = Order.objects.all().prefetch_related('items__product').order_by('-created_at')
    serializer_class = OrderSerializer

    @action(detail=True, methods=['get'], url_path='recommend-box')
    def recommend_box(self, request, pk=None):
        """
        Custom endpoint to recommend the best box for a specific order.
        GET /api/orders/<id>/recommend-box/
        """
        order = self.get_object()
        
        # Call the recommendation service layer
        recommended_box = BoxSelectorService.select_box(order)
        
        if recommended_box is not None:
            serializer = BoxSerializer(recommended_box)
            return Response({
                "message": "Best box recommended successfully.",
                "recommended_box": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "message": "No suitable box found for this order. Check product dimensions or total weight/volume limits.",
            "recommended_box": None
        }, status=status.HTTP_200_OK)
