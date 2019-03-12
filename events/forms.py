from django import forms
from .models import Event
from django.utils import timezone


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'date', 'reminder']

        widgets = {
            'author': forms.HiddenInput(),
            'date': forms.DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd hh:mm:ss'}),
        }

    def clean_date(self):
        data = self.cleaned_data['date']
        now = timezone.now()
        if data < now:
            raise forms.ValidationError("Enter valid date")
        return data
