from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_patient, name='register_patient'),
    path("home/", views.patient_home, name="patient_home"),
    path('medical-history/', views.medical_history, name='patient_medical_history'),
    path("appointments/", views.patient_appointments, name="patient_appointments"),
   path("appointments/", views.patient_appointments, name="patient_appointments"),
    path("appointments/<int:pk>/pay/", views.pay_appointment, name="pay_appointment"),
 path('patient/resources/', views.patient_resources, name='patient_resources'),




]
