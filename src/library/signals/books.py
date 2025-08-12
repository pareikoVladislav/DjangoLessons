from django.core.mail import send_mail
from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from src.library.models import Book


@receiver(pre_save, sender=Book)
def book_pre_save_track_old_genre(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_genre = None
        return

    try:
        old = sender.objects.only('id', 'genre').get(pk=instance.pk)

        instance._old_genre = old.genre
    except sender.DoesNotExist:
        instance._old_genre = None


@receiver(post_save, sender=Book)
def book_post_save_notify_genre_change(sender, instance, created, **kwargs):
    if created:
        return

    old_genre = getattr(instance, '_old_genre', None)
    new_genre = instance.genre

    if not old_genre or old_genre == new_genre:
        return

    def _send_mail():
        subject = f"Genre changed"
        message = f"Genre of book {instance.title} was changed from '{old_genre}' -> to '{new_genre}'"
        from_mail = "no-reply.091224-ptm@gmail.com"
        to_mail = [instance.publisher.email]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_mail,
            recipient_list=to_mail,
            fail_silently=False
        )

    transaction.on_commit(_send_mail)
