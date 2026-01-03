from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import make_password
from admin_panel.models import Appointment, EducationInformation
from e_hospitality.models import CustomUser
from .models import MedicalRecord, Patient
from django.contrib.auth.decorators import login_required


def register_patient(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        insurance = request.POST.get("insurance")

        # Simple validation
        if password1 != password2:
            return render(request, "register.html", {"error": "Passwords do not match"})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists"})

        # Create user
        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=make_password(password1),
            role="patient"
        )

        # Create patient profile
        Patient.objects.create(
            user=user,
            age=age,
            gender=gender,
            insurance=insurance
        )

        return redirect("login")  # Redirect to login page after success

    return render(request, 'patient/register.html')





@login_required
def patient_appointments(request):
    appointments = Appointment.objects.select_related("doctor__user").all()
    patient = get_object_or_404(Patient, user=request.user)
    return render(request, "patient/appointments.html", {
        "appointments": appointments,
        "patient": patient,
    })

@login_required
def pay_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    patient = get_object_or_404(Patient, user=request.user)

    # Already booked or no slots
    if appointment.patients.filter(id=patient.id).exists() or appointment.available_slots() <= 0:
        return redirect("patient_appointments")

    if request.method == "POST":
        upi_id = request.POST.get("upi_id")
        # Simulate payment success (integrate real payment gateway if needed)
        if upi_id:
            appointment.patients.add(patient)
            return render(request, "patient/payment_success.html", {"appointment": appointment, "patient": patient})

    return render(request, "patient/pay_appointment.html", {"appointment": appointment, "patient": patient})






@login_required
def patient_home(request):
    return render(request, "patient/home.html")



@login_required
def medical_history(request):
   
    patient_username = request.user.username

    records = MedicalRecord.objects.filter(
        patient=request.user
    ).select_related('doctor').order_by('-record_date')

    return render(request, 'patient/medical_history.html', {
        'records': records,
        'patient_username': patient_username,
    })




def patient_resources(request):
    # Get all education posts, newest first
    posts = EducationInformation.objects.all().order_by('-created_at')
    return render(request, 'patient/resources.html', {'posts': posts})
