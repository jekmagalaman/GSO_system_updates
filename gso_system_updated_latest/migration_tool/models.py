from django.db import models

# Define available target models (app_label.ModelName)
TARGET_MODELS = [
    ('inventory.Item', 'Inventory Items'),
    ('reports.WorkAccomplishmentReport', 'Work Accomplishment Reports'),
    ('requests.Request', 'Requests'),
]

class DataMigration(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='migrations/')
    target_model = models.CharField(max_length=100, choices=TARGET_MODELS)  # dropdown
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} → {self.target_model}"
