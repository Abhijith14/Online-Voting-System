from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from .models import datastore


admin.site.register(datastore)
admin.site.site_header = 'Online Voting System'