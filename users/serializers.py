from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer as DjRestAuthRegisterSerializer
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'role',
            'owner_approval_status',
            'psid',
        ]
        read_only_fields = ['owner_approval_status']

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.get('role', User.ROLE_ANONYMOUS)
        owner_status = User.OWNER_APPROVAL_NOT_REQUESTED
        if role == User.ROLE_OWNER:
            owner_status = User.OWNER_APPROVAL_PENDING

        user = User(**validated_data, owner_approval_status=owner_status)
        user.set_password(password)
        user.save()
        return user


class DjRestAuthRoleRegisterSerializer(DjRestAuthRegisterSerializer):
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default=User.ROLE_ANONYMOUS,
        required=False,
    )

    def custom_signup(self, request, user):
        role = self.validated_data.get('role', User.ROLE_ANONYMOUS)
        owner_status = User.OWNER_APPROVAL_NOT_REQUESTED
        if role == User.ROLE_OWNER:
            owner_status = User.OWNER_APPROVAL_PENDING

        user.role = role
        user.owner_approval_status = owner_status
        user.save(update_fields=['role', 'owner_approval_status'])
