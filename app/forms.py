from django.forms import (ModelForm, TextInput, EmailInput, Select, FileInput, CharField)
from .models import PersonalInfo




class PersonalInfoForm(ModelForm):
    
   class Meta:
      model = PersonalInfo
      fields = ['photo', 'first_name', 'last_name','email_address','phone','gender','state_residence']


      widgets = {
         'photo': FileInput(attrs={'id': 'profile-pic', 'onchange': 'readURL(this);'}),

         'first_name': TextInput(attrs={'class': 'form-control scnd_form', 'data-validation': 'required'}),

         'last_name': TextInput(attrs={'class': 'form-control scnd_form', 'data-validation': 'required'}),

         'email_address': EmailInput(attrs={'class': 'form-control scnd_form', 'data-validation': 'email'}),

         'phone': TextInput(attrs={'class': 'form-control scnd_form', 'data-validation': 'required'}),

         'state_residence': TextInput(attrs={'class': 'form-control scnd_form', 'data-validation': 'required'}),

         'gender': Select(attrs={'class': 'form-control scnd_form'}),
      }  


class EduForm(ModelForm):
    
   class Meta:
      model = PersonalInfo
      fields = ['institut_name', 'admission_year', 'graduation_year','degree_type', 'course']

      widgets = {   
         'institut_name': TextInput(attrs={'class': 'form-control scnd_form', 'data-validation': 'required'}),

         'admission_year': TextInput(attrs={'class': 'form-control scnd_form datepicker', 'data-validation': 'required','data-provide':'datepicker','placeholder':'dd/mm/yyyy', 'data-date-format':'dd/mm/yyyy'}),

         'graduation_year': TextInput(attrs={'class': 'form-control scnd_form datepicker', 'data-validation': 'required','data-provide':'datepicker','placeholder':'dd/mm/yyyy', 'data-date-format':'dd/mm/yyyy'}),

         'degree_type': Select(attrs={'class': 'form-control scnd_form', 'data-validation': 'required'}),

         'course': TextInput(attrs={'class': 'form-control scnd_form', 'data-validation': 'required'})
      }  


class OthersForm(ModelForm):
    
   class Meta:
      model = PersonalInfo
      fields = [ 'skills','cert_body','cert_qualification','tracks']

      widgets = {
         'skills': TextInput(attrs={'class': 'form-control scnd_form', 'placeholder': 'E.g. Team work, Excel, Communication', 'data-validation':'required'}),

         'cert_body': TextInput(attrs={'class': 'form-control scnd_form'}),

         'cert_qualification': TextInput(attrs={'class': 'form-control scnd_form'}),
         'tracks': Select(attrs={'class': 'form-control scnd_form'}),
      }        