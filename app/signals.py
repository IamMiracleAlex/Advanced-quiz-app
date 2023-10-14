from django.conf import settings
from django.dispatch import receiver
from django.urls import reverse

from allauth.account.signals import user_signed_up
from pinax.referrals.models import Referral

from .models import PersonalInfo
from assessment.models import Student



@receiver(user_signed_up)
def create_personal_info(sender, **kwargs):
    request = kwargs['request'] 
    user = kwargs['user']

    refer = Referral.create(user=user, redirect_to=reverse('account_signup'), label ="Link Created")
    
    personalinfo = PersonalInfo(user=user, referral=refer, email_address=user.email)
    personalinfo.save()

    Referral.record_response(request, "Link Created")

    Student.objects.create(user=user)





