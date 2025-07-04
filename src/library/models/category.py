from django.db import models

class Category(models.Model):
    title: str = models.CharField(
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.title
