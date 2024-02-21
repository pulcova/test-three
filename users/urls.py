from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

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

    # Doctor login, signup, dashboard, staff-list
    path('doctor/login/', views.doctorLogin, name='doctor-login'),
    path('doctor/logout/', views.doctorLogout, name='doctor-logout'),
    path('doctor/', views.doctorDashboard, name='doctor-dashboard'),
    path('doctor/profile/', views.doctorProfile, name='doctor-profile'),
    path('doctor/update-profile/', views.doctorUpdateProfile, name='doctor-update-profile'),
    path('doctor/delete-profile/', views.doctorDeleteProfile, name='doctor-delete-profile'),
    path('doctor/staff-list', views.staffList, name='doctor-staff-list'),

    # Patient login, signup, dashboard, guidelines
    path('patient/login/', views.patientLogin, name='patient-login'),
    path('patient/signup/', views.patientSignup, name='patient-signup'),
    path('patient/logout/', views.patientLogout, name='patient-logout'),
    path('patient/', views.patientDashboard, name='patient-dashboard'),
    path('patient/guide/', views.patientGuidelines, name='patient-guide'),
    path('patient/profile/', views.patientProfile, name='patient-profile'),
    path('patient/update-profile/', views.patientUpdateProfile, name='patient-update-profile'),
    path('patient/delete-profile/', views.patientDeleteProfile, name='patient-delete-profile'),

    # Staff login, signup, dashboard, patient-list
    path('staff/login/', views.staffLogin, name='staff-login'),
    path('staff/logout/', views.staffLogout, name='staff-logout'),
    path('staff/', views.staffDashboard, name='staff-dashboard'),
    path('staff/profile/', views.staffProfile, name='staff-profile'),
    path('staff/update-profile/', views.staffUpdateProfile, name='staff-update-profile'),
    path('staff/delete-profile/', views.staffDeleteProfile, name='staff-delete-profile'),

    # Password reset for user, doctor, patient, staff
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/login/', RedirectView.as_view(url='/')),


    path('health-records/', views.redirect_to_docs_dashboard, name='health_records'),
]