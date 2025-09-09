from django.contrib import admin
from .models import WorkAccomplishmentReport

@admin.register(WorkAccomplishmentReport)
class WorkAccomplishmentReportAdmin(admin.ModelAdmin):
    list_display = (
        "date_started", "date_completed", "request_type", 
        "requesting_office", "assigned_personnel", "status", "rating"
    )
