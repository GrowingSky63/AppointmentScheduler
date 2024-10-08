# scheduling/forms.py

from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'doctor', 'scheduled_time', 'reason']
        widgets = {
            'doctor': forms.HiddenInput(),
            'scheduled_time': forms.HiddenInput(),
        }
