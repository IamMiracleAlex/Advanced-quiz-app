import json

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site
from django.utils.html import format_html
from django.db.models.functions import TruncDay
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import path, reverse
from django.contrib import messages

from allauth.account.models import EmailAddress
from allauth.account.admin import EmailAddressAdmin

from .models import (PersonalInfo, UserMetric, MassMail, PersonalInfoMetric)
from .mixins import ExportCsvMixin
from .utils import EmailHandler


User = get_user_model()

# admin.site.unregister(Site)
admin.site.unregister(User)


@admin.register(User)
class UserA(UserAdmin, ExportCsvMixin):
    actions = ["export_as_csv"] 
    date_hierarchy = 'date_joined'
    ExportCsvMixin.export_as_csv.short_description = 'Export users to csv'


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin, ExportCsvMixin):
    date_hierarchy = 'created_at'
    list_display = ('first_name', 'last_name', 'email_address','phone',
        'created_at','completed', 'tracks','taken_test', 'state_residence', 'updated_at')
    raw_id_fields = ('user',)
    list_filter = ('taken_test','degree_type','completed','tracks')
    search_fields = ('first_name', 'last_name', 'email_address', 'phone')
    actions = ["export_as_csv", 'set_incomplete']
    ExportCsvMixin.export_as_csv.short_description = 'Export selected to csv'

    # def mark_completed(self, request, queryset): 
    #     queryset.update(completed = True) 
    #     messages.success(request, "Selected applications have been marked as completed!") 
  
    def set_incomplete(self, request, queryset): 
        queryset.update(completed = False) 
        messages.success(request, "Selected applications has been set to incompleted!") 


@admin.register(UserMetric)
class UserMetricAdmin(admin.ModelAdmin):
    change_list_template = 'admin/usermetric_change_list.html'

    def changelist_view(self, request, extra_context=None):
        # Aggregate new users per day
        chart_data = (
            UserMetric.objects.annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        response = super().changelist_view(
            request, extra_context=extra_context,)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        # Count of all users
        metrics = {
            'total': Count('id'),
        }
    
        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        return response

    def get_urls(self):
        # Url for async data reload
        urls = super().get_urls()
        custom_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        return custom_urls + urls


    def chart_data_endpoint(self, request):
        # returns data as json
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        # helper function for aggregating users
        return (
            UserMetric.objects.annotate(date=TruncDay("date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )



@admin.register(PersonalInfoMetric)
class PersonalInfoMetricAdmin(admin.ModelAdmin):
    change_list_template = 'admin/personalinfometric_change_list.html'

    def changelist_view(self, request, extra_context=None):
        # Aggregate new p_info per day
        chart_data = (
            PersonalInfoMetric.objects.annotate(date=TruncDay("updated_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        response = super().changelist_view(
            request, extra_context=extra_context,)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        # Count of all users
        metrics = {
            'total': Count('id'),
        }
    
        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        return response

    def get_urls(self):
        # Url for async data reload
        urls = super().get_urls()
        custom_urls = [
            path("chart/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        return custom_urls + urls


    def chart_data_endpoint(self, request):
        # returns data as json
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        # helper function for aggregating users
        return (
            PersonalInfoMetric.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )



class MassMailAdmin(admin.ModelAdmin):
    model = MassMail

    list_display = ('subject','created','author','updated','updated_by','custom_actions')
    search_fields = ['subject',]
    list_filter = ['created', 'updated']
    exclude = ['author','updated_by']


    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.author = request.user
            obj.updated_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


    def get_urls(self):
        # handles send mail url
        urls = super().get_urls()
        my_urls = [
            path('<int:mail_id>/mail/', self.admin_site.admin_view(self.send_email), name='send_email')
        ]
        return my_urls + urls

    def custom_actions(self, obj):
        # Send mail button
        return format_html(
            '<a class="button" href="{}">Send Mail</a>',
            reverse('admin:send_email', args=[obj.id])
        )
    
    custom_actions.short_description = 'Email all Users'

    def send_email(self, request, mail_id, *args, **kwargs):
        self.process_mail(
            request=request,
            mail_id=mail_id,
        )

        self.message_user(request, f'Success, has been sent to all users.')
        # self.message_user(request, f'Success, "{obj.subject}" has been sent to all users.')
       
        return HttpResponseRedirect(reverse("admin:app_massmail_changelist"))


    def process_mail(self, request, mail_id): 
        # get all emails, pass get mail contents and pass them to EmailThread to send email
        
        emails = [ p.email for p in User.objects.all() ] 

        obj = self.get_object(request, mail_id) 

        EmailHandler(obj.subject, obj.message, emails).run()




admin.site.register(MassMail, MassMailAdmin)