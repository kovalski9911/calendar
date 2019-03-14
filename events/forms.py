from django import forms
from .models import Event
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


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


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(label="Username", max_length=15)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
