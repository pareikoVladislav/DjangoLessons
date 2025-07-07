from uuid import uuid4

from django.db import models
from django.utils import timezone


class Post(models.Model):
    id: uuid4 = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    title: str = models.CharField(
        max_length=255,
        unique_for_date="created_at",
    )
    content: str = models.TextField()
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    moderated = models.BooleanField(
        default=False,
    )
    created_at: timezone = models.DateTimeField(
        auto_now_add=True
    )
    updated_at: timezone = models.DateTimeField(
        auto_now=True
    )
    library = models.ForeignKey(
        'Library',
        on_delete=models.CASCADE,
        related_name='posts'
    )
