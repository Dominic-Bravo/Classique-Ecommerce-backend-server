# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_OWNER = 'owner'
    ROLE_CUSTOMER = 'customer'
    ROLE_ANONYMOUS = 'anonymous'

    ROLE_CHOICES = [
        (ROLE_OWNER, 'Owner'),
        (ROLE_CUSTOMER, 'Customer'),
        (ROLE_ANONYMOUS, 'Anonymous'),
    ]

    OWNER_APPROVAL_NOT_REQUESTED = 'not_requested'
    OWNER_APPROVAL_PENDING = 'pending'
    OWNER_APPROVAL_APPROVED = 'approved'
    OWNER_APPROVAL_REJECTED = 'rejected'

    OWNER_APPROVAL_CHOICES = [
        (OWNER_APPROVAL_NOT_REQUESTED, 'Not requested'),
        (OWNER_APPROVAL_PENDING, 'Pending'),
        (OWNER_APPROVAL_APPROVED, 'Approved'),
        (OWNER_APPROVAL_REJECTED, 'Rejected'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_ANONYMOUS)
    owner_approval_status = models.CharField(
        max_length=20,
        choices=OWNER_APPROVAL_CHOICES,
        default=OWNER_APPROVAL_NOT_REQUESTED,
    )
    psid = models.CharField(max_length=255, unique=True, null=True, blank=True)

    @property
    def is_approved_owner(self):
        return (
            self.role == self.ROLE_OWNER
            and self.owner_approval_status == self.OWNER_APPROVAL_APPROVED
        )
