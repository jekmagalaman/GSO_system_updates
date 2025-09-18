from django.urls import path
from . import views

urlpatterns = [
    path('gso-inventory/', views.gso_inventory, name='gso_inventory'),

    # CRUD
    path('add/', views.add_inventory_item, name='add_inventory_item'),
    path('update/<int:item_id>/', views.update_inventory_item, name='update_inventory_item'),
    path('delete/<int:item_id>/', views.remove_inventory_item, name='remove_inventory_item'),




    # Unit Head Inventory URL
    path('unit-head-inventory/', views.unit_head_inventory, name='unit_head_inventory'),


    # Personnel Inventory URL
    path('personnel-inventory/', views.personnel_inventory, name='personnel_inventory'),
]
