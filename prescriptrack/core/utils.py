# core/utils.py
from PIL import Image
from django.http import HttpResponse
from pyzbar.pyzbar import decode
from core.email_utils import send_alert_email

from .models import AccessLog

from .mailer import send_alert  
from .mailer import send_alert
from django.utils import timezone
from datetime import timedelta

def extract_qr_hash(image_path):
    image = Image.open(image_path)
    decoded_objects = decode(image)
    for obj in decoded_objects:
        return obj.data.decode('utf-8')  # Return the hash inside QR
    return None
# If you separate into mailer.py


def check_for_fraud(prescription):
    logs = AccessLog.objects.filter(prescription=prescription)

    if logs.count() > 1:
        send_alert(
            subject="🚨 Duplicate Prescription Detected",
            message=f"Prescription ID {prescription.prescription_id} was scanned multiple times.\nPatient: {prescription.patient.name}\nDoctor: {prescription.doctor.name}"
        )
        return "⚠️ Duplicate Usage Detected"

    if prescription.date_issued < timezone.now() - timedelta(days=5):
        send_alert(
            subject="⏰ Expired Prescription Scan Attempt",
            message=f"Prescription ID {prescription.prescription_id} is expired.\nIssued on: {prescription.date_issued}\nPatient: {prescription.patient.name}"
        )
        return "⏰ Expired Prescription"

    return "✅ All Clear"


def verify_qr_and_flag(rx_id):
    # Your logic to scan QR and detect fraud
    is_fraudulent = check_fraud(rx_id)  # pyright: ignore[reportUndefinedVariable] # Replace with your logic
    if is_fraudulent:
        send_alert_email(rx_id)


def verify_prescription(request):
    rx_id = request.POST.get("rx_id")
    verify_qr_and_flag(rx_id)
    return HttpResponse("Verification complete.")