from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    )
from .models import Event
from django.urls import reverse_lazy
from .forms import EventForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

# Добавить проверку на подтверждение пользователя после регистрации для CBV


class EventCreateView(LoginRequiredMixin, CreateView):
    """Class for creating new event"""

    login_url = reverse_lazy('users:login')
    model = Event
    template_name = 'events/event_create.html'
    form_class = EventForm
    success_url = reverse_lazy('events:event-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EventListView(LoginRequiredMixin, ListView):
    """Class for a list of event"""

    login_url = reverse_lazy('users:login')
    model = Event

    def get_queryset(self):
        now = timezone.now()
        q = Event.objects.filter(start_date__gt=now)
        return q


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Class for a deleting event"""

    model = Event
    success_url = reverse_lazy('events:event-list')

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        else:
            return False
