from django.contrib import admin
from django.forms import TextInput, Textarea

from django.db import models

# Register your models here.
from .models import datastore


class datastoreAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


admin.site.register(datastore, datastoreAdmin)
admin.site.site_header = 'Online Voting System'