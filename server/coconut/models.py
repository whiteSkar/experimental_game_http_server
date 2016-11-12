from django.db import models

import datetime


class User(models.Model):
    user_name = models.CharField(max_length=64)
    device_id = models.CharField(max_length=256)
    creation_date = models.DateTimeField()
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.user_name