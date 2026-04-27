# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('customer', 'Customer'),
        ('anonymous', 'Anonymous'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    psid = models.CharField(max_length=255, unique=True, null=True, blank=True)