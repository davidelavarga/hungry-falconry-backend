from django.contrib import admin
from .models import Feeder, Schedule, Hub

# Register your models here.
admin.site.register(Feeder)
admin.site.register(Schedule)
admin.site.register(Hub)
