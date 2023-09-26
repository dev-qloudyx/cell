
from django.core.mail import EmailMessage
from celery import shared_task

@shared_task
def send_mail_after_delay(email_subject, email_body, from_email, recipient_list):
    mail = EmailMessage(email_subject, email_body, from_email, recipient_list)
    mail.send()

    return f"Task created"