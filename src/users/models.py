from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager

class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(unique= True,max_length=254, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return f"email: {self.email}"