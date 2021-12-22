from django.db import models
from users.models import CustomUser
from django.db.models.deletion import CASCADE

from groups.models import MyGroup
# Create your models here.

class Topic(models.Model):
    """Topic that the user is learning."""

    CHOICES = (('priv', 'private'),
                      ('pub', 'public'),
                      ('grp', 'group')
                     )

    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    access = models.CharField(max_length=10, choices=CHOICES, default="priv")
    owner = models.ForeignKey(CustomUser, on_delete=CASCADE)
    group = models.ForeignKey(MyGroup, on_delete=CASCADE, blank=True, null=True)
    


    def __str__(self):
        return self.text


class Entry(models.Model):
    """Informations about your learning progres."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(CustomUser, on_delete=CASCADE);

    class Meta:
        """Pomocnicza klasa, ktora przechowuje dodatkowe przyfdatne informacje podrzac zarzadzania modelami"""
        verbose_name_plural = "entries"

    def __str__(self):
        return self.text if  len(self.text) < 50 else f"{self.text[:50]}..."