from django.db import models
from django.conf import settings

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.username} ({self.specialization})"





