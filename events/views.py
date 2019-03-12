from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  )
from .models import Event
from django.urls import reverse_lazy


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
