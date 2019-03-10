from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .tasks import send_testing_email


class Reminder(models.Model):
    class Meta:
        pass

    name = models.CharField(
        verbose_name='Reminder name',
        max_length=100,
    )

    def __str__(self):
        return self.name


class Event(models.Model):
    class Meta:
        pass

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name='Event name',
        max_length=100,
    )

    date = models.DateTimeField(
        verbose_name='Event date',
    )

    reminder = models.ForeignKey(
        Reminder,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    reminder_date = models.DateTimeField(
        verbose_name='Дата напоминания',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


def create_reminder_date(**kwargs):
    if kwargs['created']:
        if str(kwargs['instance'].reminder) == 'remind for 1 hour':
            kwargs['instance'].reminder_date = kwargs['instance'].date - timedelta(hours=1)
            kwargs['instance'].save()
        elif str(kwargs['instance'].reminder) == 'remind for 2 hours':
            kwargs['instance'].reminder_date = kwargs['instance'].date - timedelta(hours=2)
            kwargs['instance'].save()
        elif str(kwargs['instance'].reminder) == 'remind for 4 hours':
            kwargs['instance'].reminder_date = kwargs['instance'].date - timedelta(hours=4)
            kwargs['instance'].save()
        elif str(kwargs['instance'].reminder) == 'remind for 1 day':
            kwargs['instance'].reminder_date = kwargs['instance'].date - timedelta(days=1)
            kwargs['instance'].save()
        elif str(kwargs['instance'].reminder) == 'remind for a week':
            kwargs['instance'].reminder_date = kwargs['instance'].date - timedelta(days=7)
            kwargs['instance'].save()

        if kwargs['instance'].author.email:
            send_testing_email.delay(kwargs['instance'].author.email)
            send_testing_periodic_email


post_save.connect(create_reminder_date, sender=Event)
