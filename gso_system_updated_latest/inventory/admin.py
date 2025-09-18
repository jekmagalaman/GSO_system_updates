from django.contrib import admin
from .models import InventoryItem

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "quantity", "unit", "owned_by", "updated_at")
    list_filter = ("owned_by", "category")
    search_fields = ("name", "description")
