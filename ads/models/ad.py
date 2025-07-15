from django.db import models
from django.contrib.auth.models import User
from ads.models.base import TimeStampedModel

class Ad(TimeStampedModel):
    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('furniture', 'Мебель'),
        ('clothing', 'Одежда'),
        ('books', 'Книги'), 
        ('other', 'Другое'),
    ]

    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/у'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["city"]),
            models.Index(fields=["category"]),
            models.Index(fields=["condition"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self) -> str:
        return self.title
