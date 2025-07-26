# core/mailer.py
from django.core.mail import send_mail

def send_alert(subject, message):
    send_mail(
        subject,
        message,
        'wddevil888@gmail.com',  # Sender
        ['harishh1012.2005@gmail.com'],      # Receiver(s)
        fail_silently=False
    )
 