from django.contrib.auth import get_user_model

from assessment.models import Student


User = get_user_model()


for user in User.objects.all():
    Student.objects.create(user=user)