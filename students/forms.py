from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class GatekeeperLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.role != 'gatekeeper':
            raise forms.ValidationError("Access denied: You are not a gatekeeper.")

# class AttendanceFilterForm(forms.Form):
#     ATTENDANCE_CHOICES = [
#         ('class', 'Class Attendance'),
#         ('exam_start', 'Exam Attendance - Start'),
#         ('exam_end', 'Exam Attendance - End'),
#     ]

#     attendance_type = forms.ChoiceField(choices=ATTENDANCE_CHOICES, label="Attendance Type")
#     department = forms.CharField(max_length=100)
#     level = forms.CharField(max_length=20)
#     teacher_name = forms.CharField(max_length=100)