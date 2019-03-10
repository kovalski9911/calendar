from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  )
from .models import Reminder, Event
from .forms import ReminderForm
from django.urls import reverse, reverse_lazy


class ReminderListView(ListView):
    model = Reminder


class ReminderDetailView(DetailView):
    model = Reminder


class ReminderCreateView(CreateView):
    form_class = ReminderForm
    template_name = 'events/reminder_create.html'

    def get_success_url(self):
        return reverse('events:reminder-detail', kwargs={'pk': self.object.pk})


class ReminderUpdateView(UpdateView):
    form_class = ReminderForm
    model = Reminder
    template_name = 'events/reminder_create.html'

    def get_success_url(self):
        return reverse('event:reminder-detail', kwargs={'pk': self.object.pk})


class ReminderDeleteView(DeleteView):
    model = Reminder
    success_url = reverse_lazy('event:reminder-list')


#######################################

class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event_create.html'
    fields = ['name', 'date', 'reminder']
    success_url = reverse_lazy('events:reminder-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        print(form.instance.author)
        return super().form_valid(form)


class EventListView(ListView):
    model = Event