from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.

class Topic(models.Model):
    """Topic that the user is learning."""

    CHOICES = ((True, 'private'),
                      (False, 'public')
                     )

    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    access = models.BooleanField(choices=CHOICES)
    owner = models.ForeignKey(User, on_delete=CASCADE)
    

    def __str__(self):
        return self.text


class Entry(models.Model):
    """Informations about your learning progres."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=CASCADE);

    class Meta:
        """Pomocnicza klasa, ktora przechowuje dodatkowe przyfdatne informacje podrzac zarzadzania modelami"""
        verbose_name_plural = "entries"

    def __str__(self):
        return self.text if  len(self.text) < 50 else f"{self.text[:50]}..."