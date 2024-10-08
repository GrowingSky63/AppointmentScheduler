# scheduling/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Doctor, Appointment
from .forms import AppointmentForm
from datetime import datetime, timedelta, date
from django.core.paginator import Paginator


def index(request):
    # Get all unique specializations
    specializations = Doctor.objects.values_list('specialization', flat=True).distinct()
    return render(request, 'appointments.html', {'specializations': specializations})

def get_doctors(request):
    specialization = request.GET.get('specialization', None)
    doctors = []
    if specialization:
        doctors = list(Doctor.objects.filter(specialization=specialization).values('id', 'name'))
    return JsonResponse({'doctors': doctors})

def get_schedules(request):
    doctor_id = request.GET.get('doctor_id', None)
    date_str = request.GET.get('date', None)
    schedules = []
    if doctor_id and date_str:
        doctor = Doctor.objects.get(id=doctor_id)
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        # Assuming 'shift_hours' is a string like '08:00-16:00'
        start_time_str, end_time_str = doctor.shift_hours.split('-')
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()

        # Generate time slots at 30-minute intervals
        current_datetime = datetime.combine(selected_date, start_time)
        end_datetime = datetime.combine(selected_date, end_time)
        delta = timedelta(minutes=30)
        while current_datetime < end_datetime:
            # Check if this time slot is available
            appointment_exists = Appointment.objects.filter(
                doctor=doctor,
                scheduled_time=current_datetime
            ).exists()
            if not appointment_exists:
                schedules.append(current_datetime.strftime('%H:%M'))
            current_datetime += delta
    return JsonResponse({'schedules': schedules})


def available_appointments(request):
    doctor_id = request.GET.get('doctor_id', None)
    schedule = request.GET.get('schedule', None)
    appointments = []
    if doctor_id and schedule:
        doctor = Doctor.objects.get(id=doctor_id)
        # For simplicity, assuming appointments are for today
        appointment_time = datetime.combine(date.today(), datetime.strptime(schedule, '%H:%M').time())
        existing_appointments = Appointment.objects.filter(doctor=doctor, scheduled_time=appointment_time)
        if not existing_appointments.exists():
            # Time slot is available
            appointments.append(f"Horário disponível: {schedule}")
        else:
            appointments.append(f"Horário indisponível: {schedule}")
    return JsonResponse({'appointments': appointments})

def appointment_success(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'appointment_success.html', {'appointment': appointment})

def appointment_create(request):
    doctor_id = request.GET.get('doctor_id', None)
    schedule = request.GET.get('schedule', None)
    date_str = request.GET.get('date', None)
    initial_data = {}
    doctor_name = ''
    scheduled_time_formatted = ''
    if doctor_id and schedule and date_str:
        doctor = Doctor.objects.get(id=doctor_id)
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        scheduled_time = datetime.combine(selected_date, datetime.strptime(schedule, '%H:%M').time())
        initial_data = {
            'doctor': doctor.id,
            'scheduled_time': scheduled_time
        }
        doctor_name = doctor.name
        scheduled_time_formatted = scheduled_time.strftime('%d/%m/%Y %H:%M')
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            # Redirect to appointment success page with appointment ID
            return redirect('appointment_success', appointment_id=appointment.id)
    else:
        form = AppointmentForm(initial=initial_data)
    return render(request, 'appointment_form.html', {
        'form': form,
        'doctor_name': doctor_name,
        'scheduled_time_formatted': scheduled_time_formatted
    })

def appointments_list(request):
    appointments = Appointment.objects.all()
    paginator = Paginator(appointments, 10)  # Mostra 10 consultas por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'appointment_list.html', {'page_obj': page_obj})