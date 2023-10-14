import threading

from django.conf import settings
from django.core.mail import BadHeaderError, send_mail, send_mass_mail
from django.http import HttpResponse



# class EmailThread(threading.Thread):
#     '''Sends users emails by threading. Essential for large user base. This can also be achived using Async, or Task Queue.'''

#     def __init__(self, subject, content, recipients):
#         self.subject = subject
#         self.recipients = recipients
#         self.content = content
#         threading.Thread.__init__(self)

#     def run(self):
#         msg = EmailMessage(self.subject, self.content, settings.EMAIL_HOST_USER, self.recipients)
#         msg.content_subtype = "html"
#         try:
#             msg.send()
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')


class EmailThread(threading.Thread):
    '''Sends users emails by threading. '''

    def __init__(self, subject, message, emails):
        self.subject = subject
        self.message = message
        self.emails = emails
        threading.Thread.__init__(self)

    def run(self):

        datatuple = (
        (self.subject, self.message, 'EduBridge Academy', [email]) for email  in self.emails
        )  
        
        try:
            send_mass_mail(datatuple)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')




class EmailHandler:
    '''Sends users emails by threading. Essential for large user base. This can also be achived using Async, or Task Queue.'''

    def __init__(self, subject, message, emails):
        self.subject = subject
        self.message = message
        self.emails = emails

    def run(self):

        for email in self.emails:
            send_mail(self.subject, self.message, 'EduBridge Academy', [email])



