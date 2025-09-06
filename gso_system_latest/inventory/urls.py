from django.urls import path
from . import views


urlpatterns = [
    # GSO Inventory URL
    path('gso-inventory/', views.gso_inventory, name='gso_inventory'),


    # Unit Head Inventory URL
    path('unit-head-inventory/', views.unit_head_inventory, name='unit_head_inventory'),


    # Personnel Inventory URL
    path('personnel-inventory/', views.personnel_inventory, name='personnel_inventory'),
]
