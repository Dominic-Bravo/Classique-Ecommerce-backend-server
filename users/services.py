# apps/users/services.py
from .models import User

def get_or_create_user_from_psid(psid):
    user, created = User.objects.get_or_create(
        psid=psid,
        defaults={
            "username": psid  # or generate random
        }
    )
    return user