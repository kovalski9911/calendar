from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from datetime import timedelta
from .tasks import send_email

from rest_framework.authtoken.models import Token

User = get_user_model()


class Event(models.Model):

    REMINDER_CHOICES = (
        ('1h', 'remind for 1 hour'),
        ('2h', 'remind for 2 hours'),
        ('4h', 'remind for 4 hours'),
        ('1d', 'remind for 1 day'),
        ('1w', 'remind for a week')
    )

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

    reminder = models.CharField(
        max_length=255,
        choices=REMINDER_CHOICES,
        blank=True,
        null=True
    )

    reminder_date = models.DateTimeField(
        verbose_name='Reminder date',
        blank=True,
        null=True
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name


def create_reminder_date(instance, created, **kwargs):
    if created:
        if str(instance.reminder) == '1h':
            instance.reminder_date = instance.date - timedelta(hours=1)
            instance.save()
        elif str(instance.reminder) == '2h':
            instance.reminder_date = instance.date - timedelta(hours=2)
            instance.save()
        elif str(instance.reminder) == '4h':
            instance.reminder_date = instance.date - timedelta(hours=4)
            instance.save()
        elif str(instance.reminder) == '1d':
            instance.reminder_date = instance.date - timedelta(days=1)
            instance.save()
        elif str(instance.reminder) == '1w':
            instance.reminder_date = instance.date - timedelta(days=7)
            instance.save()

        if instance.author.email:
            if instance.reminder:
                # отправка письма с напоминанием
                user_reminder_date = instance.reminder_date
                user_email = instance.author.email
                user_name = instance.author.username
                event_name = instance.name
                send_email.apply_async(args=(user_email,
                                             user_name,
                                             event_name
                                             ),
                                       eta=user_reminder_date)


post_save.connect(create_reminder_date, sender=Event)


def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


post_save.connect(create_auth_token, sender=User)
