from reminder.celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task(name="send_email_task")
def send_testing_email(user_email):
    send_mail(
        'Напоминание',
        'Вы оставили в расписании задачу',
        settings.EMAIL_HOST_USER,
        [user_email]
    )
