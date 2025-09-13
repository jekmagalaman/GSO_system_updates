from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError



class User(AbstractUser):
    ROLE_CHOICES = [
        ('gso', 'GSO Office'),
        ('unit_head', 'Unit Head'),
        ('personnel', 'Personnel'),
        ('employee', 'Employee'),
    ]

    UNIT_CHOICES = [
        ('admin', 'Admin'),
        ('requestor', 'Requestor'),
        ('maintenance', 'Maintenance'),
        ('electrical', 'Electrical'),
        ('utility', 'Utility'),
        ('motorpool', 'Motorpool'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]


    account_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='unassigned')

    def clean(self):
        # Unit Head OR Personnel must have a valid unit
        if self.role in ["unit_head", "personnel"] and self.unit in ["admin", "requestor", "unassigned"]:
            raise ValidationError(f"{self.get_role_display()} must be assigned to a valid service unit (Maintenance, Electrical, Utility, Motorpool).")

        # GSO Office and Employees should NOT be tied to service units
        if self.role in ["gso", "employee"] and self.unit not in ["admin", "requestor", "unassigned"]:
            raise ValidationError(f"{self.get_role_display()} should not be assigned to a service unit.")
