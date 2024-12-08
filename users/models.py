from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Сделать телефон необязательным
    address = models.CharField(max_length=255, blank=True, null=True)  # Сделать адрес необязательным

    def __str__(self):
        return self.user.username
