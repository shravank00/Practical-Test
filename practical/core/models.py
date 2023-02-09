from django.db import models

# Create your models here.
from django.contrib.auth.models import User 
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True)
    designation = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=255, null=True)