from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import make_password
from admin_panel.models import Appointment
from e_hospitality.models import CustomUser
from patient.models import MedicalRecord, Patient
from .models import Doctor
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages


def register_doctor(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        specialization = request.POST.get("specialization")
        department = request.POST.get("department")

        # Simple validation
        if password1 != password2:
            return render(request, "doctor_register.html", {"error": "Passwords do not match"})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, "doctor_register.html", {"error": "Username already exists"})

        # Create user
        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=make_password(password1),
            role="doctor"
        )

        # Create doctor profile
        Doctor.objects.create(
            user=user,
            specialization=specialization,
            department=department
        )

        return redirect("login")  # Redirect to login page after success

    return render(request, "doctor/register.html")





@login_required
def doctor_home(request):
    return render(request, "doctor/home.html")



@login_required
def e_prescribing(request):
    if request.method == 'POST':
        patient_username = request.POST.get('patient_username')
        diagnosis = request.POST.get('diagnosis')
        symptoms = request.POST.get('symptoms')
        medicines = request.POST.get('medicines')

        # find patient by username
        try:
            patient_user = CustomUser.objects.get(username=patient_username, role='patient')
        except CustomUser.DoesNotExist:
            messages.error(request, "Patient not found.")
            return redirect('doctor_eprescribing')

        # create medical record – doctor and date auto-saved
        MedicalRecord.objects.create(
            doctor=request.user,
            patient=patient_user,
            diagnosis=diagnosis,
            symptoms=symptoms,
            medicines=medicines,
            record_date=timezone.now()
        )

        messages.success(request, "Prescription saved successfully.")
        return redirect('doctor_eprescribing')

    return render(request, 'doctor/e_prescribing.html')




@login_required
@user_passes_test(lambda u: u.role == 'doctor')
def doctor_appointments(request):
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date', '-time')
    return render(request, 'doctor/appointments.html', {'appointments': appointments})




@login_required
@user_passes_test(lambda u: u.role == 'doctor')
def doctor_patient_management(request):
    query = request.GET.get('q', '').strip()
    patients = []
    if query:
        # case-insensitive startswith
        patients = Patient.objects.filter(user__username__istartswith=query)
    return render(request, 'doctor/patient_management.html',
                  {'patients': patients, 'query': query})

@login_required
@user_passes_test(lambda u: u.role == 'doctor')
def patient_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    records = MedicalRecord.objects.filter(patient=patient.user).order_by('-record_date')
    return render(request, 'doctor/patient_history.html',
                  {'patient': patient, 'records': records})