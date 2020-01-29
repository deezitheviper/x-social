from django.db import models
from django.urls import reverse
from django.conf import settings 
from django.contrib.auth import get_user_model
from groups.models import Group
from django.utils.text import slugify 
# Create your models here.
User = get_user_model()
class Post(models.Model):
    name = models.CharField(max_length=250,blank=False,default='')
    content = models.TextField(blank=False, default='')
    post_time = models.TimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    group = models.ForeignKey(Group,related_name='posts', on_delete=models.CASCADE)
    content_html = models.TextField(blank=True,editable=False, default='')
    slug = models.SlugField(allow_unicode=True,unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
       self.slug = slugify(self.name)
       self.content_html = (self.content)
       super().save(*args, **kwargs) # Call the real save() method    

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"username":self.user.username,"slug": self.slug})

    class Meta:
        ordering = ['-post_time']  
        unique_together = ['user','content']  
       
    
