# scheduling/models.py

from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    room = models.CharField(max_length=10)
    shift_hours = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    patient_name = models.CharField(max_length=100)
    reason = models.TextField()

    def __str__(self):
        return f"{self.patient_name} with {self.doctor} at {self.scheduled_time}"
