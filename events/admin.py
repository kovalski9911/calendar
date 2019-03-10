from django.contrib import admin
from .models import Reminder, Event


admin.site.register(Reminder)
admin.site.register(Event)
