from django.db import models

# Create your models here.
import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
# class Category(models.Model):
#     category_name = models.CharField(max_length=50)
    
#     def __str__(self):
#         return self.category_name

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    is_public=models.BooleanField(default=True)
    slug = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name + " ==> " + str(self.author)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + "_" + str(self.post_date))
        return super().save(*args, **kwargs)

class BlogComment(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    description = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return str(self.blog)
    
    
