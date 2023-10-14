from django.core.mail import send_mail
from django.template.loader import render_to_string

PROGRAM_DATE = '20th July, 2020'


def send_failed_test_email(profile):
    context = {'first_name': profile.first_name }
    subject = 'Career Acceleration Program Status'
    message = render_to_string('assessment/emails/failed.txt', context)
    email = profile.email_address
    send_mail(subject, message, 'EduBridge Academy', [email])


def send_passed_test_email(profile):
    context = {'first_name': profile.first_name, 'program_date': PROGRAM_DATE }
    subject = 'Welcome to Edubridge Career Acceleration Program'
    message = render_to_string('assessment/emails/passed.txt', context)
    email = profile.email_address
    send_mail(subject, message, 'EduBridge Academy', [email])
