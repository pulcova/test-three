from django.urls import path
from . import views

urlpatterns = [
    # Landing page
    path('', views.landingPage, name='landing-page'),

    # User login, signup, dashboard
    path('user/', views.userPage, name='user-page'),    
    path('login/', views.userLogin, name='login'),
    path('signup/', views.userSignup, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Doctor login, signup, dashboard
    path('doctor/login/', views.doctorLogin, name='doctor-login'),
    path('doctor/logout/', views.doctorLogout, name='doctor-logout'),
    path('doctor/', views.doctorDashboard, name='doctor-dashboard'),

    # Patient login, signup, dashboard``
    path('patient/login/', views.patientLogin, name='patient-login'),
    path('patient/signup/', views.patientSignup, name='patient-signup'),
    path('patient/logout/', views.patientLogout, name='patient-logout'),
    path('patient/', views.patientDashboard, name='patient-dashboard'),
    path('patient/guide/', views.patientGuidelines, name='patient-guide'),

    # Staff login, signup, dashboard
    path('staff/login/', views.staffLogin, name='staff-login'),
    path('staff/logout/', views.staffLogout, name='staff-logout'),
    path('staff/', views.staffDashboard, name='staff-dashboard'),
]