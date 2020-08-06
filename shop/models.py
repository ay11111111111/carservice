from django.db import models
from django.core.validators import URLValidator
# Create your models here.

class Shop(models.Model):
    url = models.TextField(validators=[URLValidator()])
