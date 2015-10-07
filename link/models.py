from django.db import models


# Create your models here.

class MyUrl(models.Model):

    link_to = models.CharField(max_length=500)
    short_link = models.CharField(max_length=50)

    def __str__(self):
        return self.short_link
