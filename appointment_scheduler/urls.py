# views.py

from django.contrib import admin
from django.urls import path
from scheduling import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='doctor_list'),
    path('get_doctors/', views.get_doctors, name='get_doctors'),
    path('get_schedules/', views.get_schedules, name='get_schedules'),
    path('appointment/new/', views.appointment_create, name='appointment_create'),
    path('appointment/success/<int:appointment_id>/', views.appointment_success, name='appointment_success'),
    path('appointments/', views.appointments_list, name='appointments_list'),
]