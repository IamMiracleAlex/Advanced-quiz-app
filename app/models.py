from django.db import models
from django.contrib.auth import get_user_model
from pinax.referrals.models import Referral

User = get_user_model()


class PersonalInfo(models.Model):
   GENDER_CHOICES = [
       ('select_a_gender', 'Select a gender'),
      ('male', 'Male'),
     ( 'female', 'Female'),
   ]
   TRACK_CHOICES = [
      ('select_a_track', 'Select a track'), 
     ( 'industry_analysis', 'Industry Analysis (Consulting)'),
     ( 'company_research', 'Company Research (Investment Research)'),
     ( 'data_analytics', 'Data Analytics'),
     ( 'human_resources', 'Human Resources'),
     ( 'accounting', 'Accounting'),
   ]
   DEGREE_CHOICES = [
    ('select_a_degree', 'Select a degree'),
     ( 'undergraduate', 'Undergraduate'),
     ( 'graduate', 'Graduate'),
     ( 'postgraduate', 'Post Graduate'),
   ]

   
   user                       = models.ForeignKey(User,  on_delete=models.CASCADE)
   photo                      =  models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True, )
   first_name                 =  models.CharField(max_length=50, null=True, blank=True)
   last_name                  =  models.CharField(max_length=50, null=True, blank=True)
   email_address              =  models.CharField(max_length=50, null=True, blank=True)
   phone                      =  models.CharField(max_length=50, null=True, blank=True)
   state_residence            =  models.CharField(max_length=50, null=True, blank=True)
   gender                     =  models.CharField(max_length=50, default='select_a_gender', choices=GENDER_CHOICES, blank=True)
   institut_name              =  models.CharField(max_length=100, null=True, blank=True)
   admission_year             =  models.CharField(max_length=50, null=True, blank=True)
   graduation_year            =  models.CharField(max_length=50, null=True, blank=True)
   degree_type                =  models.CharField(max_length=50, default='select_a_degree', choices=DEGREE_CHOICES, blank=True)
   course                     =  models.CharField(max_length=100, null=True, blank=True)
   tracks                     = models.CharField(max_length=50, blank=True, default='select_a_track', choices=TRACK_CHOICES)
   skills                     =  models.CharField(max_length=255, null=True, blank=True)
   cert_body                  =  models.CharField(max_length=150, null=True, blank=True)
   cert_qualification         =  models.CharField(max_length=50, null=True, blank=True)
   created_at                 = models.DateTimeField(auto_now_add=True)
   updated_at                 = models.DateTimeField(auto_now=True)
   completed                  = models.BooleanField(default=False, help_text='Whether user has completed application')
   taken_test                 = models.BooleanField(default=False, help_text='Whether user has taken test')
   referral                   = models.ForeignKey(Referral, on_delete=models.SET_NULL, null=True, blank=True)
 
   class Meta:
      verbose_name_plural = "Personal Information"


class MassMail(models.Model):
    subject = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='massmails', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='massmail_update', null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name_plural = "Mass Mail"



class UserMetric(User):

    class Meta:
        proxy = True
        verbose_name_plural = 'User Metrics'


class PersonalInfoMetric(PersonalInfo):

    class Meta:
        proxy = True
        verbose_name_plural = 'Personal Information Metrics'

