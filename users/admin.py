from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# custom user admin 
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username',
        'email',
        'role',
        'owner_approval_status',
        'is_staff',
        'is_superuser',
    ]
    list_filter = [
        'role',
        'owner_approval_status',
        'is_staff',
        'is_superuser',
        'is_active',
    ]
    actions = ['approve_owner_requests', 'reject_owner_requests']
    fieldsets = UserAdmin.fieldsets + (
        ('Classique role approval', {
            'fields': ('role', 'owner_approval_status', 'psid'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Classique role approval', {
            'fields': ('role', 'owner_approval_status', 'psid'),
        }),
    )
    # get readonly func
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly_fields.extend(['role', 'owner_approval_status'])
        return readonly_fields

    def approve_owner_requests(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, 'Only superadmins can approve owners.', level='error')
            return

        updated = queryset.filter(role=User.ROLE_OWNER).update(
            owner_approval_status=User.OWNER_APPROVAL_APPROVED
        )
        self.message_user(request, f'{updated} owner request(s) approved.')

    approve_owner_requests.short_description = 'Approve selected owner requests'

    def reject_owner_requests(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, 'Only superadmins can reject owners.', level='error')
            return

        updated = queryset.filter(role=User.ROLE_OWNER).update(
            owner_approval_status=User.OWNER_APPROVAL_REJECTED
        )
        self.message_user(request, f'{updated} owner request(s) rejected.')

    reject_owner_requests.short_description = 'Reject selected owner requests'
