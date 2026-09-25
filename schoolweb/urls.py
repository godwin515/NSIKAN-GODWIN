from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('admissions/', views.admissions, name='admissions'),
    path('academics/', views.academics, name='academics'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.events, name='events'),
    path('apply/', views.apply, name='apply'),
    path('application-success/<str:reference>/', views.application_success, name='application_success'),
    path('test-email/', views.test_email, name='test_email'),
    
    
    # student-related URLs
    path('students/login/',     views.student_login,     name='student_login'),
    path('students/logout/',    views.student_logout,    name='student_logout'),
    path('students/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('students/results/',   views.check_result,      name='check_result'),
]