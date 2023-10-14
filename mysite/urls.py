from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url




urlpatterns = [
    path('', include('app.urls')),
    url(r'accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    url(r'^referrals/', include('pinax.referrals.urls', namespace='pinax_referrals')),
    path('', include('assessment.urls')),
]
