from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib import admin
# Create your models here.


class CustomUser(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    role = models.CharField(max_length=20, choices=ROLES)

    groups = models.ManyToManyField(
            "auth.Group",
            related_name="customuser_set",
            related_query_name="customuser",
            blank=True,
            help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
            verbose_name="groups",
        )

    user_permissions = models.ManyToManyField(
            "auth.Permission",
            related_name="customuser_set",
            related_query_name="customuser",
            blank=True,
            help_text="Specific permissions for this user.",
            verbose_name="user permissions",
        )
 

