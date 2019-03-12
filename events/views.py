from django.views.generic import (
    ListView,
    CreateView,
    TemplateView,
    )
from .models import Event
from django.urls import reverse_lazy
from .forms import EventForm
from django.contrib.auth.mixins import LoginRequiredMixin


class EventCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('events:login')
    model = Event
    template_name = 'events/event_create.html'
    form_class = EventForm
    success_url = reverse_lazy('events:event-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        print(form.instance.author)
        return super().form_valid(form)


class EventListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('events:login')
    model = Event
