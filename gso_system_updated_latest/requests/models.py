from django.db import models
from django.conf import settings
from inventory.models import InventoryItem

class ServiceRequest(models.Model):
    UNIT_CHOICES = [
        ('repair and maintenance', 'Repair and Maintenance'),
        ('utility', 'Utility'),
        ('electrical', 'Electrical'),
        ('motorpool', 'Motorpool'),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("In Progress", "In Progress"),
        ("Done for Review", "Done for Review"),
        ("Completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    
    requestor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)




    full_name = models.CharField(max_length=255, blank=True, null=True)  # <-- add this
    email = models.EmailField(blank=True, null=True)  # optional if you want to save
    contact_number = models.CharField(max_length=50, blank=True, null=True)  # optional



    
    assigned_personnel = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="assigned_requests"
    )


    materials = models.ManyToManyField(
        InventoryItem,              # use import
        through='RequestMaterial',
        blank=True,
        related_name="requests"
    )



    def __str__(self):
        return f"Request #{self.id} - {self.get_unit_display()}"





class RequestMaterial(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    material = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.material.name} x {self.quantity} for Request #{self.request.id}"