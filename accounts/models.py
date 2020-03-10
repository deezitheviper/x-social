from django.db import models
from django.contrib import auth  

# Create your models here.
class User(auth.models.User,auth.models.PermissionsMixin):
    avatar = models.ImageField(upload_to='media/avatar/', default='media/avatar/icons8-administrator-male-50.png') 

    def __str__(self):
        return "@{}".format(self.username)
    
