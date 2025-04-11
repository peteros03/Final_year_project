from django.contrib import admin
from django.contrib import messages
import subprocess
from django.utils.html import format_html
from .models import Student
from .nfc_utils import write_nfc_url, NFCWriteError
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

from .models import Campus, College, School, Department, Level, Student

# # Write NFC URL action
# def write_nfc_url_action(modeladmin, request, queryset):
#     # Check if the NFC reader is connected and write URL to NFC
#     for student in queryset:
#         success = write_nfc_url(student)
#         if success:
#             modeladmin.message_user(request, f"NFC URL for {student.student_id} written successfully!")
#         else:
#             modeladmin.message_user(request, f"Failed to write NFC for {student.student_id}. Check NFC reader.")

# # Register the action
# write_nfc_url_action.short_description = "Write NFC URL to selected students"

#class StudentAdmin(admin.ModelAdmin):
    #list_display = ('student_id', 'first_name', 'last_name', 'profile_url')
   
# Define the action to write NFC URL
def write_nfc_url_action(modeladmin, request, queryset):
    for student in queryset:
        try:
            # Attempt to write the NFC URL
            success = write_nfc_url(student)
            if success:
                modeladmin.message_user(request, f"NFC URL for {student.id} written successfully!", level=messages.SUCCESS)
        except NFCWriteError as e:
            modeladmin.message_user(request, f"Error: {e}", level=messages.ERROR)

# Register the action for the Student model
write_nfc_url_action.short_description = "Write NFC URL to selected students"



class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'profile_url', 
        'get_department', 'get_school', 'get_college', 'get_campus',
        'level', 'finance_status', 'laptop_serial', 'academic_year'
    )
    
   
    search_fields = ['name', 'id']
    list_filter = ['department', 'school', 'college', 'level', 'finance_status']
    actions = [write_nfc_url_action]

    def profile_url(self, obj):
        url = obj.get_profile_url()
        return format_html('<a href="{}" target="_blank">{}</a>', url, url)
    profile_url.short_description = "Profile URL"

    
    #def get_profile_url(self, obj):
        #return f'<a href="{obj.get_profile_url()}">{obj.get_profile_url()}</a>'
    
    #get_profile_url.allow_tags = True
    #get_profile_url.short_description = 'Profile URL'

    def get_department(self, obj):
        return obj.level.department
    get_department.short_description = 'Department'

    def get_school(self, obj):
        return obj.level.department.school
    get_school.short_description = 'School'

    def get_college(self, obj):
        return obj.level.department.school.college
    get_college.short_description = 'College'

    def get_campus(self, obj):
        return obj.level.department.school.college.campus
    get_campus.short_description = 'Campus'
    
# Custom User Admin class
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # List of fields to display in the admin panel
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    # Fields to be used for searching users in the admin panel
    search_fields = ('username', 'email', 'role')
    # Fields that will be used to filter the user list
    list_filter = ('role', 'is_staff', 'is_active')
    # Fields for user details
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Role', {'fields': ('role',)}),  # Add the role field here
    )
    # Add ordering by username
    ordering = ('username',)

# Register the CustomUser model with the CustomUserAdmin

admin.site.register(CustomUser, CustomUserAdmin)    
admin.site.register(Campus)
admin.site.register(College)
admin.site.register(School)
admin.site.register(Department)
admin.site.register(Level)
admin.site.register(Student, StudentAdmin)


