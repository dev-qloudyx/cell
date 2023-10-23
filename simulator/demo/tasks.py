
from django.core.mail import EmailMessage
from celery import shared_task


@shared_task
def send_mail_after_delay(email_subject, email_body, from_email, recipient_list, video_file, report_file):
    mail = EmailMessage(email_subject, email_body, from_email, recipient_list)
    mail.attach_file(video_file)
    mail.attach_file(report_file)
    mail.send()

    return f"task finished"


@shared_task
def send_mail_after_delay_2(email_subject, email_body, from_email, recipient_list):
    mail = EmailMessage(email_subject, email_body, from_email, recipient_list)
    mail.send()

    return f"task finished"