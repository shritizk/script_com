from django.db import models

# Create your models here.
class emailCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=64, unique=True)