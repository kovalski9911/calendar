from django.views.generic import (
    ListView,
    CreateView,
    TemplateView,
    )
from .models import Event
from django.urls import reverse_lazy
from .forms import EventForm


class WelcomeView(TemplateView):
    template_name = 'events/login.html'


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event_create.html'
    form_class = EventForm
    success_url = reverse_lazy('events:event-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        print(form.instance.author)
        return super().form_valid(form)


class EventListView(ListView):
    model = Event
