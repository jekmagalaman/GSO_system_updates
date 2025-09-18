from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    UNIT_CHOICES = [
        ("Piece (pcs)", "Piece (pcs)"),
        ("Unit", "Unit"),
        ("Set", "Set"),
        ("Box", "Box"),
        ("Pack", "Pack"),
        ("Roll", "Roll"),
        ("Meter (m)", "Meter (m)"),
        ("Sheet", "Sheet"),
        ("Bag", "Bag"),
        ("Bottle", "Bottle"),
        ("Liter", "Liter"),
        ("Gallon", "Gallon"),
        ("Kit", "Kit"),
    ]

    CATEGORY_CHOICES = [
        ("Furniture & Fixtures", "Furniture & Fixtures"),
        ("Electronics & IT Equipment", "Electronics & IT Equipment"),
        ("Electrical Supplies", "Electrical Supplies"),
        ("Building Materials & Hardware", "Building Materials & Hardware"),
        ("Cleaning & Janitorial Supplies", "Cleaning & Janitorial Supplies"),
        ("Tools & Maintenance", "Tools & Maintenance"),
        ("Safety & Security Equipment", "Safety & Security Equipment"),
    ]

    unit = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = InventoryItem
        fields = ['name', 'description', 'quantity', 'unit', 'category',]
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"}),
            'quantity': forms.NumberInput(attrs={"class": "form-control"}),
            'owned_by': forms.HiddenInput(),
        }
