# accounts/services/user_services.py
from django.core.exceptions import ValidationError
from ..models import User
from django.db import IntegrityError

def add_user(data: dict) -> User:
    username = data.get("username")
    password = data.get("password")
    email = data.get("email", "")
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    bio = data.get("bio", "")
    avatar = data.get("avatar", "")
    grupo = data.get("grupo", "Leitor")

    # Validações manuais
    if not username or not password:
        raise ValidationError("Username and password are required fields.")
    if len(password) < 7:
        raise ValidationError("Password must be at least 8 characters long.")

    try:
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            avatar=avatar,
            grupo=grupo,
        )
        user.set_password(password)  # Armazena a senha de forma segura
        user.save()
        return user
    except IntegrityError:
        raise ValidationError("Username already exists.")
