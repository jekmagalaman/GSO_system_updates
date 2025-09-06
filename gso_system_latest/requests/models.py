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
