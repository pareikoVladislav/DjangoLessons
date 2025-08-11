from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.choices.base import Role
from src.users.models import User


@receiver(post_save, sender=User)
def notify_admin_on_new_moderator(sender, instance, created, **kwargs):
    if created and instance.is_staff and instance.role == Role.employee.lower():
        mail_text = "Moderator {} was added to the system. You can message him via his email: {}"

        recipients_email = [
            user.email for user in User.objects.filter(role=Role.reader.lower())
        ]

        send_mail(
            subject='New moderator in the system',
            message=mail_text.format(instance.username, instance.email),
            from_email='no-reply.091224-ptm@gmail.com',
            recipient_list=recipients_email
        )
