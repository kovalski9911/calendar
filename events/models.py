from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import timedelta
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


def create_reminder_date(instance, created, **kwargs):
    if created:
        if str(instance.reminder) == 'remind for 1 hour':
            instance.reminder_date = instance.date - timedelta(hours=1)
            instance.save()
        elif str(instance.reminder) == 'remind for 2 hours':
            instance.reminder_date = instance.date - timedelta(hours=2)
            instance.save()
        elif str(kwargs['instance'].reminder) == 'remind for 4 hours':
            instance.reminder_date = instance.date - timedelta(hours=4)
            instance.save()
        elif str(instance.reminder) == 'remind for 1 day':
            instance.reminder_date = instance.date - timedelta(days=1)
            instance.save()
        elif str(instance.reminder) == 'remind for a week':
            instance.reminder_date = instance.date - timedelta(days=7)
            instance.save()

        if instance.author.email:
            # отправка письма с напоминанием
            user_reminder_date = instance.reminder_date
            user_email = instance.author.email
            send_testing_email.apply_async(args=(user_email,), eta=user_reminder_date)


post_save.connect(create_reminder_date, sender=Event)
