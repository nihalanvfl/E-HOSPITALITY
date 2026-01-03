# admin_panel/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone


class Appointment(models.Model):
    doctor = models.ForeignKey('doctor.Doctor', on_delete=models.CASCADE, related_name='appointments')
    location_name = models.CharField(max_length=150)
    date = models.DateField()
    time = models.TimeField()
    total_slots = models.PositiveIntegerField()
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # NEW
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_appointments'
    )
    patients = models.ManyToManyField('patient.Patient', blank=True, related_name='appointments')

    def available_slots(self):
        return self.total_slots - self.patients.count()

    def __str__(self):
        return f"{self.doctor.user.username} | {self.date} {self.time} | {self.location_name} | ${self.fee}"




class EducationInformation(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(help_text="Short description or intro.")
    content = models.TextField(help_text="Full health education content.")
    resources_link = models.URLField(blank=True, null=True, help_text="Optional link to external resources")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Health Education Resource"
        verbose_name_plural = "Health Education Resources"

    def __str__(self):
        return self.title