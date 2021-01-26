from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    location=models.CharField(max_length=200)


class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=500)
    content=models.TextField()
    likes=models.IntegerField(default=0)
    created_on=models.DateField(default=date.today)

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog instance.
        """
        return reverse('postdetail', args=[str(self.pk)])


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    c_author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    parent=models.ForeignKey('Comment',null=True,blank=True,on_delete=models.CASCADE)
    likes=models.IntegerField(default=0)
    created_on=models.DateTimeField(auto_now_add=True)