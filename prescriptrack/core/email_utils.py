from django.core.mail import send_mail
from django.conf import settings

def send_alert_email(rx_id):
    subject = "⚠️ Prescription Fraud Alert"
    message = f"Fraud detected in RX ID: {rx_id}. Please review immediately."
    recipient = ['harishh1012.2005@gmail.com']
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient)