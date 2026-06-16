from typing import Optional, List
from decimal import Decimal
from django.core.exceptions import ValidationError
from core.models import Box, Order, OrderItem


class BoxSelectorService:
    """
    Service layer responsible for selecting the best packaging box for an order.
    """

    @staticmethod
    def select_box(order: Order) -> Optional[Box]:
        """
        Recommends the best box for a given Order.
        
        Selection Criteria:
        1. All products must physically fit inside the box dimensions (allowing rotation).
        2. The total weight of the order must not exceed the box's max_weight.
        3. Returns the cheapest valid box.
        4. If there is a tie on cost, returns the box with the smallest inner volume.

        Edge cases handled:
        - Empty order: Returns None.
        - Invalid quantities (e.g. <= 0): Raises ValidationError.
        - No valid box: Returns None.
        """
        items = order.items.all()
        if not items:
            return None

        # 1. Validate order items (e.g., check for invalid quantities)
        BoxSelectorService._validate_order_items(items)

        # 2. Calculate total order weight
        total_weight = BoxSelectorService._calculate_total_weight(items)

        # 3. Calculate total order volume (pre-requisite for volume check)
        total_volume = BoxSelectorService._calculate_total_volume(items)

        # 4. Prepare list of sorted product dimensions to check fitment
        product_dimensions_list = BoxSelectorService._get_sorted_product_dimensions(items)

        valid_boxes: List[Box] = []

        # 5. Filter boxes
        for box in Box.objects.all():
            # Check weight constraint
            if total_weight > box.max_weight:
                continue

            # Check total volume constraint (heuristic for fitting multiple items)
            if total_volume > box.volume:
                continue

            # Check if each product's dimensions can physically fit (allowing rotation)
            if not BoxSelectorService._check_dimensions_fit(product_dimensions_list, box):
                continue

            valid_boxes.append(box)

        if not valid_boxes:
            return None

        # 6. Sort valid boxes by cost (ascending), then volume (ascending)
        valid_boxes.sort(key=lambda b: (b.cost, b.volume))

        return valid_boxes[0]

    @staticmethod
    def _validate_order_items(items) -> None:
        """
        Validates that all order items have valid positive quantities.
        Raises ValidationError if any item is invalid.
        """
        for item in items:
            if item.quantity <= 0:
                raise ValidationError(
                    f"Invalid quantity {item.quantity} for product '{item.product.name}'. Quantity must be greater than zero."
                )

    @staticmethod
    def _calculate_total_weight(items) -> Decimal:
        """
        Calculates the total weight of all items in the order.
        """
        return sum(item.product.weight * item.quantity for item in items)

    @staticmethod
    def _calculate_total_volume(items) -> Decimal:
        """
        Calculates the total volume of all items in the order.
        """
        return sum(item.product.volume * item.quantity for item in items)

    @staticmethod
    def _get_sorted_product_dimensions(items) -> List[List[Decimal]]:
        """
        Extracts and sorts the dimensions of all products in the order.
        Returns a list of sorted dimension lists.
        """
        dims = []
        for item in items:
            # Sort individual product dimensions ascending (e.g. [height, width, length])
            sorted_dims = sorted([item.product.length, item.product.width, item.product.height])
            dims.append(sorted_dims)
        return dims

    @staticmethod
    def _check_dimensions_fit(product_dims_list: List[List[Decimal]], box: Box) -> bool:
        """
        Checks if every product in the list fits in the box's inner dimensions.
        Allows for 3D rotation by sorting the box dimensions as well.
        """
        box_sorted_dims = sorted([box.inner_length, box.inner_width, box.inner_height])
        
        for prod_dims in product_dims_list:
            # Compare each sorted dimension: shortest, medium, longest
            if (prod_dims[0] > box_sorted_dims[0] or 
                prod_dims[1] > box_sorted_dims[1] or 
                prod_dims[2] > box_sorted_dims[2]):
                return False
        return True
