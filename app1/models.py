from django.db import models

# Create your models here.

class add_c_model(models.Model):
    id = models.IntegerField(primary_key=True)
    Candidate = models.CharField(max_length=2000, default='')
    Category = models.CharField(max_length=2000, default='')
    Votes = models.IntegerField(default=0)

    def __str__(self):
        # return str(self.Candidate)
        return str(self.Candidate)
    class Meta:
        verbose_name = "Add Candidates"

