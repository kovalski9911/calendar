from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
import uuid
from django.db.models import signals
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from rest_framework.authtoken.models import Token

import datetime
import os.path
import requests
from icalendar import Calendar


class UserAccountManager(BaseUserManager):
    """Custom manager"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')

        if not password:
            raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['is_verified'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    email = models.EmailField(
        'email',
        unique=True,
        blank=False,
        null=False
    )
    full_name = models.CharField(
        'full name',
        blank=True,
        null=True,
        max_length=400
    )
    # Поместить список стран отдельно в бд
    country = models.CharField(
        'country',
        blank=True,
        null=True,
        max_length=100
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False
    )
    is_active = models.BooleanField(
        'active',
        default=True
    )
    is_verified = models.BooleanField(
        'verified',
        default=False
    )
    verification_uuid = models.UUIDField(
        'Unique Verification UUID',
        default=uuid.uuid4
    )

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __unicode__(self):
        return self.email


def user_post_save(sender, created, instance, signal, *args, **kwargs):
    """
    Send mail after register user
    Add events for users country
    """
    # Send verification email
    if not instance.is_verified:
        send_mail(
            'Verify your account',
            'Follow this link to verify your account: '
            'http://localhost:8000%s' % reverse('verify', kwargs={
                'uuid': str(instance.verification_uuid)}),
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
        )

    # add events for users country
    if instance.is_verified:
        if instance.country:
            # save ics file to local disk
            url = 'https://www.officeholidays.com/ics/ics_country.php?tbl_country={country}'.format(
                country=instance.country
            )

            file_name = '{country}.ics'.format(country=instance.country)
            file_path = 'events/event/{}'.format(file_name)

            if not os.path.isfile(file_path):
                # в зависимости от ситуации необходимо перехватить возможрные исключения
                r = requests.get(url)
                file = open('events/event/{}'.format(file_name), 'wb')
                for some in r:
                    file.write(some)
                file.close()

            # parse ics file and create a new events
            file = open('events/event/{}'.format(file_name), 'rb')
            cal = Calendar.from_ical(file.read())
            for component in cal.walk():
                if component.name == "VEVENT":
                    # only actual events
                    if component.get('dtstart').dt < datetime.date.today():
                        continue
                    else:
                        from events.models import Event
                        event = Event.objects.create(
                            author=instance,
                            name=component.get('summary'),
                            start_date=component.get('dtstart').dt,
                            stop_date=component.get('dtend').dt
                        )
                        event.save()
            file.close()


signals.post_save.connect(user_post_save, sender=User)


def create_auth_token(instance=None, created=False, **kwargs):
    """Create token after create users"""
    if created:
        Token.objects.create(user=instance)


signals.post_save.connect(create_auth_token, sender=User)
