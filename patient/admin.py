from django.contrib import admin

from patient.models import MedicalRecord, Patient


admin.site.register(Patient)
admin.site.register(MedicalRecord)

# Register your models here.
