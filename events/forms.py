from django import forms
from .models import Reminder, Event


class ReminderForm(forms.ModelForm):

    class Meta:
        model = Reminder
        fields = ['name']


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'date', 'reminder']

        widgets = {
            'author': forms.HiddenInput(),
        }
