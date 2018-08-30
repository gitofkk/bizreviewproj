from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from cities.models import Country, Region

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

class Address(models.Model):
    flat_no = models.CharField(max_length=200)
    building_name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __unicode__(self):
        return '%s %s' % (self.country, self.region)

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    verify_code = models.CharField(max_length=200, default=get_random_string)
    is_active = models.BooleanField(default=False)
