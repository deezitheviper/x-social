from django.db import models
from django.utils.text import slugify 
from django.contrib.auth import get_user_model
from django import template
from django.urls import reverse



# Create your models here.
User = get_user_model()
register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(blank=False, default='')
    slug = models.SlugField(allow_unicode=True,unique=True)
    description_html =models.TextField(blank=True,editable=False, default='')
    members = models.ManyToManyField(User,through="GroupMember")



    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
       self.slug = slugify(self.name)
       self.description_html = (self.description)
       super().save(*args, **kwargs)
       

    def get_absolute_url(self):
        return reverse("groups:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['name']
     



class GroupMember(models.Model):
    group = models.ForeignKey(Group,related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)
    

    class Meta:
      unique_together = ('user','group')

    def __str__(self):
        return self.user.name

    
