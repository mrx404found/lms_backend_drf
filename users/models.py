from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLES = (
    ("admin", "Admin"),
    ("teacher", "Teacher"),
    ("student", "Student"),
)

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=USER_ROLES)
    mobile_no = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
