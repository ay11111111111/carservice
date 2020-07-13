from django.db import models
from users.models import CustomUser
# Create your models here.



class Service(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CTO(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    rating = models.DecimalField(blank=True, default=0, max_digits=10, decimal_places=1)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    # reviews = models.ForeignKey(Review, blank=True, null=True, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)


    def __str__(self):
        return self.name
#    timetable

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CTO = models.ForeignKey(CTO, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    message = models.TextField()

    def __str__(self):
        return self.user.email
