from django.views.generic import (
    ListView,
    CreateView,
    FormView,
    DeleteView,
    )
from .models import Event
from django.urls import reverse_lazy
from .forms import EventForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone


class EventCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('events:login')
    model = Event
    template_name = 'events/event_create.html'
    form_class = EventForm
    success_url = reverse_lazy('events:event-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EventListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('events:login')
    model = Event

    def get_queryset(self):
        now = timezone.now()
        q = Event.objects.filter(start_date__gt=now)
        return q


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('events:event-list')

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        else:
            return False


# class UserRegisterView(FormView):
#     form_class = UserRegisterForm
#     success_url = reverse_lazy('events:login')
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
