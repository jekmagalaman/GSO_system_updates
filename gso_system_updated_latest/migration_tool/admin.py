from django.contrib import admin
from django import forms
from django.apps import apps
from .models import DataMigration
from .utils import process_migration


class DataMigrationForm(forms.ModelForm):
    class Meta:
        model = DataMigration
        fields = ['name', 'file', 'target_model']


@admin.register(DataMigration)
class DataMigrationAdmin(admin.ModelAdmin):
    form = DataMigrationForm
    list_display = ('name', 'target_model', 'created_at')

    def save_model(self, request, obj, form, change):
        # ✅ First save object and file to disk
        super().save_model(request, obj, form, change)

        # ✅ Now the file is guaranteed to exist
        app_label, model_name = obj.target_model.split('.')
        model = apps.get_model(app_label, model_name)

        # ✅ Use the absolute file path
        process_migration(obj.file.path, model)
