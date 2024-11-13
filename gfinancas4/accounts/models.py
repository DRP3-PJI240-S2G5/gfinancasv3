from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    avatar = models.URLField(max_length=1024, null=True, blank=True)
    grupo = models.CharField(max_length=256)

    def __str__(self):
        return str(self.username)

    def to_dict_json(self):
        return {
            "id": self.id,
            "name": self.get_full_name(),
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "avatar": self.avatar,
            "bio": self.bio,
            "permissions": {
                "ADMIN": self.is_superuser,
                "STAFF": self.is_staff,
            },
            "grupo": self.grupo, #[group.name for group in self.groups.all()]
        }
    
    def to_minimal_dict_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.avatar,
            "email": self.bio,
            "grupo": self.grupo,
        }
