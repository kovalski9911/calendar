from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminder.settings')
app = Celery('reminder')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(30.0, send_testing_periodic_email, expires=10)
#
#
# @app.task(name="send_email_periodic_task")
# def send_testing_periodic_email(user_email):
#     send_mail(
#         'heading testing msg',
#         'body testing msg',
#         settings.EMAIL_HOST_USER,
#         [user_email]
#     )
