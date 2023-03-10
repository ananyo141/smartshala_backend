from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=60)
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["email", "name"]

    def __str__(self):
        return f"{self.email}"
