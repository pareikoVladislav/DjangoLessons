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
        max_length=100
    )
    content: str = models.TextField(
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        'UserProfile',
        # on_delete=models.CASCADE,
        # on_delete=models.SET_NULL,
        # null=True,
        # on_delete=models.SET_DEFAULT,
        # default=lambda: UserProfile.objects.filter(role='admin').first(),
        # on_delete=models.SET(),
        # on_delete=models.DO_NOTHING,
        on_delete=models.PROTECT,
        related_name='posts',
        null=True,
        blank=True
    )
    created_at: datetime = models.DateTimeField(
        auto_now_add=True
    )
    updated_at: datetime = models.DateTimeField(
        auto_now=True
    )
    reading_time: int = models.DurationField(
        null=True,
        blank=True
    )
    screenshot = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True
    )
    attachment = models.FileField(
        upload_to='files/',
        null=True,
        blank=True
    )
    published_time = models.TimeField(
        null=True,
        blank=True
    )


class UserProfile(models.Model):
    full_name = models.CharField(
        max_length=60
    )
    bio = models.TextField()
    slug = models.SlugField(
        unique=True
    ) # часть URL как мой full_name
    subscriptions = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        null=True,
        blank=True
    )
    age = models.PositiveSmallIntegerField(null=True, blank=True) # 32767
    followers_count = models.BigIntegerField(null=True, blank=True)
    posts_count = models.PositiveIntegerField(null=True, blank=True)
    comments_count = models.PositiveIntegerField(null=True, blank=True)
    reputation_score = models.FloatField(null=True, blank=True)
    monetization_income = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        null=True,
        blank=True
    )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
