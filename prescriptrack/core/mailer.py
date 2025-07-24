# core/mailer.py
from django.core.mail import send_mail

def send_alert(subject, message):
    send_mail(
        subject,
        message,
        'system@prescriptrack.com',  # Sender
        ['harishh.1012.2005@gmail.com'],      # Receiver(s)
        fail_silently=False
    )
 