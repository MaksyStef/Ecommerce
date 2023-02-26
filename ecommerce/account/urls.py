from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('settings/', views.SettingsView.as_view(), name="settings"),
]
