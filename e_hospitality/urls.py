from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.user_login, name="login"),
    path("doctor/", include("doctor.urls")),
    path("patient/", include("patient.urls")),
    path("admin-panel/", include("admin_panel.urls")),
]
