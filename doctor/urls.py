# doctor/urls.py
from django.urls import path
from . import views

urlpatterns = [
        path('register/', views.register_doctor, name='register_doctor'),
        path("home/", views.doctor_home, name="doctor_home"),
        path('eprescribing/', views.e_prescribing, name='doctor_eprescribing'),
        path('appointments/', views.doctor_appointments, name='doctor_appointments'),
         path('patients/', views.doctor_patient_management, name='doctor_patient_management'),
        path('patients/<int:patient_id>/history/', views.patient_history, name='doctor_patient_history'),




   
]
