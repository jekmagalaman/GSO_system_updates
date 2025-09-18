from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = [
        ('gso', 'GSO Office'),       # Admin of the system
        ('unit_head', 'Unit Head'),
        ('personnel', 'Personnel'),
        ('requestor', 'Requestor'),  # Departments (Registrar, Cashier, etc.)
    ]

    UNIT_CHOICES = [
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
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, blank=True, null=True)

    # Only relevant if role="requestor"
    department = models.CharField(max_length=255, blank=True, null=True)

    def clean(self):
        # GSO Office should not be tied to a unit
        if self.role == "gso" and self.unit:
            raise ValidationError("GSO Office should not be assigned to a unit.")

        # Unit Head and Personnel must have a valid service unit
        if self.role in ["unit_head", "personnel"] and not self.unit:
            raise ValidationError(f"{self.get_role_display()} must be assigned to a valid service unit (Maintenance, Electrical, Utility, Motorpool).")

        # Requestors should not have a service unit
        if self.role == "requestor" and self.unit:
            raise ValidationError("Requestor accounts should not have a service unit.")

        # First/Last name required for real people (not requestors)
        if self.role in ["gso", "unit_head", "personnel"] and (not self.first_name or not self.last_name):
            raise ValidationError(f"{self.get_role_display()} accounts must have a first and last name.")

        # Requestors: no first/last name, must have department
        if self.role == "requestor":
            if self.first_name or self.last_name:
                raise ValidationError("Requestor accounts should not have first/last name.")
            if not self.department:
                raise ValidationError("Requestor accounts must have a department name.")

    def __str__(self):
        return self.department or f"{self.first_name} {self.last_name}" or self.username
