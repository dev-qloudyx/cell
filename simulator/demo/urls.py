from django.urls import path
from .views import ClientForm, MainForm
from . import views

urlpatterns = [
    path("", MainForm.as_view(), name="simulator"),
    path("success/", ClientForm.as_view(), name="client"),
    
]