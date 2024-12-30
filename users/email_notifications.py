# email_notifications.py
from django.core.mail import send_mail
from django.conf import settings


def send_approval_email(employee, job, company_name):
    subject = f"Application Approved by {company_name}"
    recipient = employee.email
    message = f"Dear {employee.first_name},\n\nYour application for the {job.title} position at {company_name} has been approved."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])

def send_rejection_email(employee, job, company_name):
    subject = f"Application Rejected by {company_name}"
    recipient = employee.email
    message = f"Dear {employee.first_name},\n\nYour application for the {job.title} position at {company_name} has been rejected."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
