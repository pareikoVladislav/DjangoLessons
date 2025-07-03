from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4


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
    content: str = models.TextField(
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        'Member',
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True
    )
    moderated = models.BooleanField(
        default=False,
    )
    created_at: datetime = models.DateTimeField(
        auto_now_add=True
    )
    updated_at: datetime = models.DateTimeField(
        auto_now=True
    )
    library = models.ForeignKey(
        'Library',
        on_delete=models.CASCADE,
        related_name='posts'
    )

