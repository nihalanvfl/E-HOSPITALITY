from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.decorators import login_required,user_passes_test

from admin_panel.models import Appointment, EducationInformation
from doctor.models import Doctor
from django.utils import timezone

@login_required
def admin_home(request):
    return render(request, "admin_panel/home.html")



@login_required
@user_passes_test(lambda u: u.role == 'admin')
def admin_appointment_management(request):
    appointments = Appointment.objects.filter(creator=request.user).order_by('-date')
    return render(request, 'admin_panel/appointment_management.html', {'appointments': appointments})


# Create appointment slot (already shown earlier)
@login_required
@user_passes_test(lambda u: u.role == 'admin')
def create_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        location_name = request.POST.get('location_name')
        date = request.POST.get('date')
        total_slots = request.POST.get('total_slots')
        time = request.POST.get('time')
        


        doctor = Doctor.objects.get(id=doctor_id)
        fee = request.POST.get('fee')

        Appointment.objects.create(
            doctor=doctor,
            location_name=location_name,
            date=date,
            time=time,
            total_slots=total_slots,
            fee=fee,
            creator=request.user
        )
        return redirect('admin_appointment_management')

    doctors = Doctor.objects.all()
    return render(request, 'admin_panel/create_appointment.html', {'doctors': doctors})


# Edit an existing appointment slot
@login_required
@user_passes_test(lambda u: u.role == 'admin')
def edit_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, creator=request.user)

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        appointment.doctor = Doctor.objects.get(id=doctor_id)
        appointment.location_name = request.POST.get('location_name')
        appointment.date = request.POST.get('date')
        appointment.time = request.POST.get('time')
        appointment.total_slots = request.POST.get('total_slots')
        appointment.fee = request.POST.get('fee')
        appointment.save()
        return redirect('admin_appointment_management')

    doctors = Doctor.objects.all()
    return render(request, 'admin_panel/edit_appointment.html', {'appointment': appointment, 'doctors': doctors})






@login_required
@user_passes_test(lambda u: u.role == 'admin')
def admin_user_management(request):
    doctors = Doctor.objects.select_related("user").all()
    return render(request, "admin_panel/user_management.html", {"doctors": doctors})

def admin_education_list(request):
    resources = EducationInformation.objects.all()
    return render(request, 'admin_panel/education_list.html', {'resources': resources})

# --- Create Page ---
def admin_education_create(request):
    if request.method == 'POST':
        EducationInformation.objects.create(
            title=request.POST.get('title'),
            summary=request.POST.get('summary', ''),
            content=request.POST.get('content'),
            resources_link=request.POST.get('resources_link', ''),
            created_at=timezone.now()
        )
        return redirect('admin_education_list')
    return render(request, 'admin_panel/education_create.html')