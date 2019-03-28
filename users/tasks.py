from reminder.celery import app

from django.contrib.sites.models import Site

import os.path
import requests
from icalendar import Calendar
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils import timezone


# добавить try except
@app.task(name="send_mail_to_verificate", default_retry_delay=5 * 60, max_retries=12)
def send_mail_to_verificate(user, *args, **kwargs):
    s = Site.objects.get_current().domain
    send_mail(
        'Verify your account',
        'Follow this link to verify your account: {0}{1}'.format(
            s,
            reverse('verify', kwargs={
                'uuid': str(user.verification_uuid)})
        ),
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


# добавить try except
@app.task(name="add_country_event", default_retry_delay=5 * 60, max_retries=12)
def add_country_event(user):
    # save ics file to local disk
    url = 'https://www.officeholidays.com/ics/ics_country.php?tbl_country={country}'.format(
        country=user.country
    )
    FILE_NAME = '{country}.ics'.format(country=user.country)
    FILE_PATH = str(settings.EVENT_DIR) + '{}'.format(FILE_NAME)

    if not os.path.isfile(FILE_PATH):
        # в зависимости от ситуации необходимо перехватить возможные исключения
        r = requests.get(url)
        file = open(FILE_PATH, 'wb')
        for some in r:
            file.write(some)
        file.close()

    # parse ics file and create a new events
    file = open(FILE_PATH, 'rb')
    cal = Calendar.from_ical(file.read())
    for component in cal.walk():
        if component.name == "VEVENT":
            # only actual events
            if component.get('dtstart').dt <= timezone.localdate():
                continue
            else:
                from events.models import Event
                event = Event.objects.create(
                    author=user,
                    name=component.get('summary'),
                    start_date=component.get('dtstart').dt,
                    stop_date=component.get('dtend').dt
                )
                event.save()
