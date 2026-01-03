from django.db import models

# Create your models here.


from django.conf import settings

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    insurance = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


class MedicalRecord(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'doctor'},
        related_name='doctor_records'       # unique reverse name
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'},
        related_name='patient_records'      # unique reverse name
    )
    diagnosis = models.TextField()
    symptoms = models.TextField()
    medicines = models.TextField()
    record_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        doc = self.doctor.username if self.doctor else "Doctor"
        return f"{self.patient.username} - {doc} - {self.record_date:%Y-%m-%d}"
