from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField('email', unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email