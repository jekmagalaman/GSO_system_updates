from django.contrib.auth.models import AbstractUser
from django.db import models

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
        ('utilities', 'Utilities'),
        ('motorpool', 'Motorpool'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]


    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, default='unassigned')
