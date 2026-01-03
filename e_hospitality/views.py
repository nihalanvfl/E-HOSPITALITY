from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")   # 🔽 capture role from form

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if hasattr(user, "role") and user.role == role:   # 🔽 check role match
                login(request, user)

                # role-based redirect
                if role == "doctor":
                    return redirect("doctor_home")
                elif role == "patient":
                    return redirect("patient_home")
                elif role == "admin":
                    return redirect("admin_home")
                else:
                    messages.error(request, "Role not recognized.")
            else:
                messages.error(request, "Role does not match the account.")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")
