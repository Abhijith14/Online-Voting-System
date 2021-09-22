from django.db import models

# Create your models here.


class datastore(models.Model):
    Categories = models.CharField(max_length=3000, default='')
    Threshold = models.IntegerField(default=1, null=False)
    Candidates = models.TextField(max_length=10000, default='')

    def __str__(self):
        return str(self.Categories) + " (" + str(len(str(self.Candidates).split(","))) + ")"

    class Meta:
        verbose_name = "Admin Database"

