from django.db import models


class Publisher(models.Model):
    name: str = models.CharField(max_length=100)
    address: str = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    city: str = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    country: str = models.CharField(max_length=100)