from django.urls import path
from . import views


urlpatterns = [
    path('consultation/<int:consultation_id>/', views.consultation_overview, name='consultation-overview')
]