from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from src.choices.base import Role
from src.users.models import User


# @receiver(post_save, sender=User)
# def notify_admin_on_new_moderator(sender, instance, created, **kwargs):
#     if created and instance.is_staff and instance.role == Role.employee.lower():
#         mail_text = "Moderator {} was added to the system. You can message him via his email: {}"
#
#         recipients_email = [
#             user.email for user in User.objects.filter(role=Role.reader.lower())
#         ]
#
#         send_mail(
#             subject='New moderator in the system',
#             message=mail_text.format(instance.username, instance.email),
#             from_email='no-reply.091224-ptm@gmail.com',
#             recipient_list=recipients_email
#         )

@receiver(post_save, sender=User)
def notify_admin_on_new_moderator(sender, instance, created, **kwargs):
    if created and instance.is_staff and instance.role == Role.employee.lower():

        subject = "New Moderator"
        sender = "no-reply.091224-ptm@gmail.com"
        recipient = "ich1.admin@gmail.com"

        context = {
            "username": instance.username,
            "email": instance.email
        }

        text_context = render_to_string(
            template_name='email_newsletters/new_moderator.txt',
            context=context
        )

        html_context = render_to_string(
            template_name='email_newsletters/new_moderator.html',
            context=context
        )

        message = EmailMultiAlternatives(
            subject=subject,
            body=text_context,
            from_email=sender,
            to=[recipient],
            headers={'List-Unsubscribe': '<mailto:test.mail@gmail.com>'}
        )

        message.attach_alternative(html_context, "text/html")

        message.send()
