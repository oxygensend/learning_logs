from django.db import models
from django.contrib.auth.models import Group
from users.models import CustomUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

# Create your models here.


class MyGroup(Group):

    admin = models.ForeignKey(CustomUser, on_delete=CASCADE)
    class meta:
        proxy=True
