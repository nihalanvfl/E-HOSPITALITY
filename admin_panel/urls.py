from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.admin_home, name="admin_home"),
    path("appointments/create/", views.create_appointment, name="admin_appointment_create"),
    path("appointments/", views.admin_appointment_management, name="admin_appointment_management"),
    path("appointments/<int:pk>/edit/", views.edit_appointment, name="admin_appointment_edit"),
    path("users/doctors/", views.admin_user_management, name="admin_user_management"),
    path('education/', views.admin_education_list, name='admin_education_list'),
   
    path('education/create/', views.admin_education_create, name='admin_education_create'),
]
