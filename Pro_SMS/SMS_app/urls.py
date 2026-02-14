from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Student URLs
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/register/', views.student_register, name='student_register'),
    path('student/profile/<int:student_id>/', views.student_profile, name='student_profile'),  # Student profile with ID
    
    # Teacher URLs
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/register/', views.teacher_register, name='teacher_register'),
    path('teacher/profile/<int:teacher_id>/', views.teacher_profile, name='teacher_profile'),
    
    # Parent URLs
    path('parent/', views.parent_dashboard, name='parent_dashboard'),
    path('parent/login/', views.parent_login, name='parent_login'),
    path('parent/child/<int:student_id>/', views.parent_view_child, name='parent_view_child'),
    
    path('logout/', views.logout_view, name='logout'),
]