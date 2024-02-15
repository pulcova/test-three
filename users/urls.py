from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.doctorLogin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logoutUser, name='logout'),

    path('user/', views.userPage, name='user-page'),

    path('doctor/', views.doctorDashboard, name='doctor-dashboard'),
    path('patient/', views.patientDashboard, name='patient-dashboard'),
    path('staff/', views.staffDashboard, name='staff-dashboard'),
]