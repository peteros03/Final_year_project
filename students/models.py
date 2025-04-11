from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
#from .models import Student 
# Create your models here.


class Campus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class College(models.Model):
    name = models.CharField(max_length=100)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/')
    laptop_serial = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=10)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    PAID = 'Paid'
    PENDING = 'Pending'
    UNPAID = 'Unpaid'

    FINANCE_STATUS_CHOICES = [
        (PAID, 'Paid'),
        (PENDING, 'Pending'),
        (UNPAID, 'Unpaid'),
    ]

    finance_status = models.CharField(
        max_length=7,
        choices=FINANCE_STATUS_CHOICES,
        default=PENDING,
    )

    def __str__(self):
        return self.name

   
    
    def get_profile_url(self):
        return f"http://localhost:8000/profile/{self.id}/"  # Or replace with your real domain
    


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('gatekeeper', 'Gatekeeper'),
        ('teacher', 'Teacher'),
        ('registrar', 'Registrar'),
        ('finance', 'Finance'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    def __str__(self):
        return self.username

# class Attendance(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)  # The student for whom attendance is being marked
#     date = models.DateField()  # The date of attendance
#     status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])  # Attendance status
#     attendance_type = models.CharField(max_length=10, choices=[('Class', 'Class'), ('Exam', 'Exam')])  # Class or exam attendance
#     teacher_name = models.CharField(max_length=255)  # Teacher's name to appear on the report
#     created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the attendance was recorded

#     def __str__(self):
#         return f"{self.student.name} - {self.status} on {self.date}"

# class ClassAttendance(models.Model):
#     ATTENDANCE_TYPES = [
#         ('class', 'Class'),
#         ('exam_start', 'Exam Start'),
#         ('exam_end', 'Exam End'),
#     ]

#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     date = models.DateField(auto_now_add=True)
#     department = models.CharField(max_length=100)
#     level = models.CharField(max_length=20)
#     attendance_type = models.CharField(max_length=20, choices=ATTENDANCE_TYPES)
#     status = models.CharField(max_length=10, default='present')  # NFC marks as 'present'

#     def __str__(self):
#         return f"{self.student.full_name} - {self.attendance_type} on {self.date}"
