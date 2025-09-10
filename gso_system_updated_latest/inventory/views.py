from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#GSO Inventory Views
@login_required
def gso_inventory(request):
    return render(request, 'gso_office/inventory/gso_inventory.html')








# Unit Head Inventory Views
@login_required
def unit_head_inventory(request):
    return render(request, 'unit_heads/unit_head_inventory/unit_head_inventory.html')

# Personnel Inventory Views
@login_required
def personnel_inventory(request):
    return render(request, 'personnel/personnel_inventory/personnel_inventory.html')