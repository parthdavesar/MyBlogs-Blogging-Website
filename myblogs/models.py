from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils import timezone   

# Create your models here.

class contact_info(models.Model):
    u_email = models.EmailField()
    u_message = models.CharField(max_length=200)
    def __str__(self):
        return self.u_email

class blog_category(models.Model):
    blog_cat = models.CharField(max_length=60, unique=True)
    blogcat_img = models.ImageField(upload_to='images/')
    blogcat_description = models.CharField(max_length=200)
    def __str__(self):
        return self.blog_cat

class blog_post(models.Model):
    blog_name = models.CharField(max_length=60)
    cover_img = models.ImageField(upload_to='images/')
    blog_description = RichTextField(blank=True)
    blog_cat = models.ForeignKey(blog_category, on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0, null=True)
    view_count = models.IntegerField(default=0, null=True)
    def __str__(self):
        return self.blog_name
    
class subscription_info(models.Model):
    s_email = models.EmailField(unique=True)
    def __str__(self):
        return self.s_email
    
class Comment(models.Model):
    post = models.ForeignKey(blog_post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.text
    
class likes(models.Model):
    post = models.ForeignKey(blog_post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)