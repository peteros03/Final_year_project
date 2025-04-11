from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('profile/<str:student_id>/', views.student_profile, name='student_profile'),
    path('', views.home_page, name='home'), 
     # Temporary login placeholder views
    path('registrar/login/', views.registrar_login, name='registrar_login'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('gatekeeper/login/', views.gatekeeper_login, name='gatekeeper_login'),
    path('finance/login/', views.finance_login, name='finance_login'),
    #path('gatekeeper/login/', views.gatekeeper_login, name='gatekeeper_login'),
    path('gatekeeper/dashboard/', views.gatekeeper_dashboard, name='gatekeeper_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Redirect to home after logout
    #path('gatekeeper/dashboard/student/<str:student_id>/', views.student_profile_view, name='student_profile_view'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]


