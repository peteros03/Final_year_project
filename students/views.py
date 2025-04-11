from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth import authenticate, login
from .forms import GatekeeperLoginForm
from .models import Student
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from .decorators import gatekeeper_required
from .decorators import teacher_required
#from .models import Profile 

@login_required
@gatekeeper_required
def student_profile(request, student_id):
    student = Student.objects.get(id=student_id)
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'students/student_profile.html', {'student': student})
    
def home_page(request):
    return render(request, 'home.html')

#simples login views
def registrar_login(request):
    return HttpResponse("Registrar login page")
def teacher_login(request):
    return HttpResponse("Teacher login page")
def gatekeeper_login(request):
    return HttpResponse("Gatekeeper login page")
def finance_login(request):
    return HttpResponse("Finance login page")
# Temporary login placeholder views

###gatekeeper login view
def gatekeeper_login(request):
    if request.method == 'POST':
        form = GatekeeperLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == 'gatekeeper':  # ✅ Ensure only gatekeepers can log in here
                login(request, user)
                return redirect('gatekeeper_dashboard')
            else:
                messages.error(request, "You are not authorized to access this portal.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = GatekeeperLoginForm()
    return render(request, 'students/gatekeeper_login.html', {'form': form})

@login_required(login_url='gatekeeper_login')
def gatekeeper_dashboard(request):
    if not request.user.role == 'gatekeeper':
        messages.error(request, "Access denied. You are not authorized to view this page.")
        return redirect('gatekeeper_login')
    return render(request, 'students/gatekeeper_dashboard.html')

# # Ensure that only gatekeepers can access this view
# @login_required(login_url='gatekeeper_login')
# def student_profile_view(request, student_id):
#     if not request.user.role == 'gatekeeper':
#         messages.error(request, "Access denied. Only gatekeepers can view this page.")
#         return redirect('home')

#     student = get_object_or_404(Student, id=student_id)
#     return render(request, 'students/profile.html', {'student': student})

# This view handles attendance. Only teachers can access it.
def attendance_url(request, student_id):
    # Check if the user is logged in as a teacher
    if not request.user.role == 'teacher':
        messages.error(request, "Access denied. Only teachers can take attendance.")
        return redirect('gatekeeper_dashboard')  # Redirect to Gatekeeper dashboard if not a teacher
    
    # Get the student object for the attendance logic
    student = get_object_or_404(Student, id=student_id)
    
    # Proceed with attendance marking (you can customize this as per your logic)
    # Example: Create a new attendance record or update an existing one
    attendance, created = Attendance.objects.get_or_create(
        student=student,
        date_today=datetime.date.today(),  # Assuming you're tracking by today's date
        defaults={'status': 'Present'}  # Set status to 'Present' by default
    )
    
    if not created:
        # If attendance already exists for today, you can update it if necessary
        attendance.status = 'Present'
        attendance.save()

    # You could add logic to handle different attendance statuses (e.g. absent)
    
    # Redirect to a page where teachers can see the updated attendance status (if needed)
    messages.success(request, f"Attendance marked for {student.name}")
    return redirect('teacher_dashboard')  # Redirect to the teacher's dashboard or attendance page

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == 'teacher':
                login(request, user)
                return redirect('teacher_dashboard')
            else:
                messages.error(request, "Not a teacher account.")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'students/teacher_login.html')

@login_required(login_url='teacher_login')
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('teacher_dashboard')
    return render(request, "students/teacher_dashboard.html")

