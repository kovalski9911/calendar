from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Event

User = get_user_model()


class EventForm(forms.ModelForm):
    """Form for create event"""

    class Meta:
        model = Event
        fields = ['name', 'start_date', 'stop_date', 'reminder']

        widgets = {
            'author': forms.HiddenInput(),
            'start_date': forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd hh:mm:ss'}),
        }

    def clean_date(self):
        # доделать проверку на start stop date!!!!
        data = self.cleaned_data['start_date']
        now = timezone.now()
        if data < now:
            raise forms.ValidationError('Enter valid date')
        return data
