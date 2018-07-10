from django.db import models


class User(models.Model):
    firstname = models.CharField(max_length=50, default='none')
    lastname = models.CharField(max_length=70, default=' ')

    username = models.CharField(max_length=32, primary_key=True)
    email = models.EmailField(max_length=50, unique=True)

    password = models.CharField(max_length=100)
    is_online = models.BooleanField(default=False)
    
    objects = models.Manager()

    def __str__(self):
        return self.username
