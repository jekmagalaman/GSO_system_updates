from django.db import models


class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(
        max_length=50,
        default="pcs",
        help_text="Unit of measurement (e.g., pcs, liters, meters, box, set)"
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Category (e.g., Electrical, Furniture, Tools, Cleaning)"
    )

    owned_by = models.CharField(
        max_length=50,
        choices=[
            ("GSO", "GSO"),
            ("Unit Head", "Unit Head"),
            ("Personnel", "Personnel"),
        ],
        default="GSO"
    )

    # 🔹 To know when an item is added or last updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🔹 Optional field to flag if item is active/removed
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
