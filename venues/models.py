# Create your models here.
from django.contrib.gis.db import models

class Venue(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.PointField(srid=4326)

    def __str__(self):
        return self.name