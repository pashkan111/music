from django.contrib.auth import get_user_model, authenticate
from ..models import User


def register_user(data: dict) -> bool:
    email = data['email']
    password = data['password']
    user = User.objects.filter(email=email)
    if user.exists():
        user = authenticate(**data)
        if not user:
            return 
        return False
    user = User.objects.create(**data)
    return True


