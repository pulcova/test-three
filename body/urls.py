from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_3d_model, name='display-3d-model'),
]