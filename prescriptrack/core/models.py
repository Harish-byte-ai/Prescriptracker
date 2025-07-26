# core/models.py
from django.contrib.auth.models import Group
from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, related_name="doctor_members")
    doctor_id = models.CharField(max_length=50, unique=True)

class Patient(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    patient_id = models.CharField(max_length=50, unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

class Prescription(models.Model):
    prescription_id = models.CharField(max_length=20)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medicine_details = models.TextField()
    date_issued = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=64)
    qr_code_image = models.ImageField(upload_to='qrcodes/')


# core/models.py
class AccessLog(models.Model):
    pharmacist_name = models.CharField(max_length=100)
    scan_time = models.DateTimeField(auto_now_add=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)
