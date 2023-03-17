from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('sign/', views.SignView.as_view(), name="sign"),
    path('logout/', views.logout_view, name="logout"),
    path('settings/', views.SettingsView.as_view(), name="settings"),
]
