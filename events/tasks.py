from reminder.celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task(name="send_email_task")
def send_email(user_email, *args, **kwargs):
    send_mail(
        'Head mail',
        'Body mail',
        settings.EMAIL_HOST_USER,
        [user_email]
    )
