import smtplib
from celery import shared_task
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from HW_skypro_Django_REST_Framework.settings import EMAIL_HOST_USER
from lms.models import Course
from users.models import SubscriptionForCourse


@shared_task
def send_course_update_message(course_id):
    """Отправляет сообщение об обновлении материалов."""

    course = Course.objects.get(course_id)
    subscriptions = SubscriptionForCourse.objects.filter(course=course_id)
    recipient_list = [subscriptions.owner.email for subscriptions in subscriptions]

    try:
        send_mail(
            subject='В курсе произошли изменения',
            message=f'В курсе "{course.title}" произошли изменения',
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=True
        )
    except BadHeaderError:
        return HttpResponse('Обнаружен недопустимый заголовок.')
    except smtplib.SMTPException:
        raise smtplib.SMTPException
