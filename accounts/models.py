from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add your custom fields here. For OTP, we need a phone number.
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    # You can add more fields like profile_picture, date_of_birth, etc.
    # For example:
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username
