from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import InventoryItem
from .forms import InventoryItemForm


# -------------------------------
# GSO Inventory (List + Search + Filter + Inline Edit/Delete)
# -------------------------------
@login_required
def gso_inventory(request):
    category = request.GET.get("category")
    query = request.GET.get("q")

    items = InventoryItem.objects.all()

    # Filter by category
    if category:
        items = items.filter(category=category)

    # Search across name, category, description
    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(description__icontains=query)
        )

    items = items.order_by("name")
    categories = InventoryItem.objects.values_list("category", flat=True).distinct()

    # Create a dictionary of forms per item (for edit modals)
    forms_per_item = {item.id: InventoryItemForm(instance=item) for item in items}

    return render(request, "gso_office/inventory/gso_inventory.html", {
        "inventory_items": items,
        "categories": categories,
        "selected_category": category,
        "search_query": query,
        "form": InventoryItemForm(),          # for Add Material modal
        "forms_per_item": forms_per_item,     # for Edit modals
    })


# -------------------------------
# Add Item
# -------------------------------
@login_required
def add_inventory_item(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("gso_inventory")


# -------------------------------
# Update Item (handled via modal)
# -------------------------------
@login_required
def update_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
    return redirect("gso_inventory")


# -------------------------------
# Delete Item (handled via modal)
# -------------------------------
@login_required
def remove_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == "POST":
        item.delete()
    return redirect("gso_inventory")




















# Unit Head Inventory Views
@login_required
def unit_head_inventory(request):
    return render(request, 'unit_heads/unit_head_inventory/unit_head_inventory.html')

# Personnel Inventory Views
@login_required
def personnel_inventory(request):
    return render(request, 'personnel/personnel_inventory/personnel_inventory.html')