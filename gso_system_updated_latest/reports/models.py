from django.db import models

class WorkAccomplishmentReport(models.Model):
    date_started = models.DateField()
    date_completed = models.DateField(null=True, blank=True)
    request_type = models.CharField(max_length=100)
    description = models.TextField()
    requesting_office = models.CharField(max_length=255)
    assigned_personnel = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    rating = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_type} - {self.description[:30]}..."
