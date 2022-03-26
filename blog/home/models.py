from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helper import *



class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.email

class BlogModel(models.Model):
    title = models.CharField(max_length = 1000)
    content = FroalaField()
    slug = models.SlugField(max_length =1000, null = True , blank = True)
    user = models.ForeignKey(User,blank=True,  null= True , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog')
    created_at =models.DateTimeField(auto_now_add=True)
    upload_to= models.DateTimeField(auto_now=True)


    def _str_(self):
        return self.title

    def save(self , *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogModel, self).save(*args, **kwargs)
