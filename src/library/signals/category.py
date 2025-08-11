from django.db.models.signals import post_save
from django.dispatch import receiver

from src.library.models import Category


@receiver(post_save, sender=Category)
def category_saved(sender, instance: Category, created: bool, **kwargs):
    print("=" * 100)
    print("=" * 100)

    print(f"Our sender is {sender}")
    if created:
        print(f"New category was created: '{instance.title}'")
    else:
        print(f"Category '{instance.title}' was updated")

    print("=" * 100)
    print("=" * 100)
