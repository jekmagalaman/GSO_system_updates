from django.db import models
from requests.models import ServiceRequest

class Material(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField()

class MaterialUsage(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_used = models.PositiveIntegerField()
