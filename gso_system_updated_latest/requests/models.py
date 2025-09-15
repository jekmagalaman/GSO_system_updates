from django.db import models
from django.conf import settings

class ServiceRequest(models.Model):
    UNIT_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('utility', 'Utility'),
        ('electrical', 'Electrical'),
        ('motorpool', 'Motorpool'),
    ]
    
    requestor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    description = models.TextField()
    status = models.CharField(default='Pending', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    
    assigned_personnel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_requests'
    )

    def __str__(self):
        return f"Request #{self.id} - {self.get_unit_display()}"