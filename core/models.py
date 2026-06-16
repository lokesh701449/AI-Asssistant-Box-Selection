from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal


class Product(models.Model):
    """
    Represents a physical product that can be ordered.
    All dimensions are in centimeters (cm) and weight in kilograms (kg).
    """
    name = models.CharField(max_length=255, unique=True, help_text="Unique name of the product")
    length = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Length of the product in cm"
    )
    width = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Width of the product in cm"
    )
    height = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Height of the product in cm"
    )
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Weight of the product in kg"
    )

    @property
    def volume(self) -> Decimal:
        """Calculate the volume of the product in cubic centimeters (cm³)."""
        return self.length * self.width * self.height

    @property
    def sorted_dimensions(self) -> list[Decimal]:
        """Returns sorted dimensions (ascending) to allow orientation-independent fitting."""
        return sorted([self.length, self.width, self.height])

    def __str__(self):
        return f"{self.name} ({self.length}x{self.width}x{self.height} cm, {self.weight} kg)"


class Box(models.Model):
    """
    Represents a box available for packaging orders.
    All dimensions are inner dimensions in centimeters (cm).
    Weight is in kilograms (kg) and cost is in currency units (e.g. USD).
    """
    name = models.CharField(max_length=255, unique=True, help_text="Unique name/type of the box")
    inner_length = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Inner length of the box in cm"
    )
    inner_width = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Inner width of the box in cm"
    )
    inner_height = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Inner height of the box in cm"
    )
    max_weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Maximum weight the box can carry in kg"
    )
    cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Cost of the box"
    )

    @property
    def volume(self) -> Decimal:
        """Calculate the inner volume of the box in cubic centimeters (cm³)."""
        return self.inner_length * self.inner_width * self.inner_height

    @property
    def sorted_dimensions(self) -> list[Decimal]:
        """Returns sorted inner dimensions (ascending) to allow orientation-independent fitting."""
        return sorted([self.inner_length, self.inner_width, self.inner_height])

    def __str__(self):
        return f"{self.name} (Cost: {self.cost}, Max Wt: {self.max_weight} kg)"


class Order(models.Model):
    """
    Represents a customer order containing one or more items.
    """
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_weight(self) -> Decimal:
        """Calculate the total weight of all items in the order in kg."""
        return sum(item.total_weight for item in self.items.all())

    @property
    def total_volume(self) -> Decimal:
        """Calculate the total volume of all items in the order in cm³."""
        return sum(item.total_volume for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} (Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"


class OrderItem(models.Model):
    """
    Represents a specific product and quantity in an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity of the product ordered"
    )

    @property
    def total_weight(self) -> Decimal:
        """Calculate total weight of this order item in kg."""
        return self.product.weight * self.quantity

    @property
    def total_volume(self) -> Decimal:
        """Calculate total volume of this order item in cm³."""
        return self.product.volume * self.quantity

    def clean(self):
        """Validate that quantity is positive."""
        super().clean()
        if self.quantity < 1:
            raise ValidationError({'quantity': "Quantity must be at least 1."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order_id}"
