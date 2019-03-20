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


def user_post_save(sender, instance, signal, *args, **kwargs):
    """Send mail after register user"""
    if not instance.is_verified:
        # Send verification email
        send_mail(
            'Verify your account',
            'Follow this link to verify your account: '
            'http://localhost:8000%s' % reverse('verify', kwargs={
                'uuid': str(instance.verification_uuid)}),
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
        )


signals.post_save.connect(user_post_save, sender=User)


def create_auth_token(instance=None, created=False, **kwargs):
    """Creating token after register users"""
    if created:
        Token.objects.create(user=instance)


signals.post_save.connect(create_auth_token, sender=User)
