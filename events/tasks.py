from reminder.celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task(name="send_email_task")
def send_email(user_email, event_name, *args, **kwargs):
    """Task for send email to user for reminder event"""
    send_mail(
        'Head mail',
        'Dear {user_email}! You event {event_name} near :)'.format(
            user_email=user_email,
            event_name=event_name
        ),
        settings.EMAIL_HOST_USER,
        [user_email]
    )
