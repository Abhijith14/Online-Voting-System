from django.db import models

from app1.models import datastore

# Create your models here.


class project(models.Model):
    id = models.AutoField(primary_key=True)
    Data = models.CharField(max_length=1000000, default="")

    def __str__(self):
        return str(self.id)

