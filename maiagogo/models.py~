from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
      author=models.ForeignKey('auth.User')
      title=models.CharField(max_length=200)
      text=models.TextField(blank=False)
      created_date=models.DateTimeField(default=timezone.now)
      published_date=models.DateTimeField(blank=True, null=True)
      
      def publish(self):
          self.published_date=timezone.now()
          self.save()
      def __unicode__(self):
          return self.title

class Comment(models.Model):
	post = models.ForeignKey('maiagogo.Post', related_name='comments')
	author=models.CharField(max_length=200)
	text=models.TextField(blank=False)
	created_date=models.DateTimeField(default=timezone.now)
	approved_comment=models.BooleanField(default=False)
	def approve(self):
	    self.approved_comment = True
	    self.save()
	def __str__(self):
	    return self.text

        def approved_comments(self):
	    return self.comments.filter(approved_comment=True)

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    likes=models.IntegerField(default=0)
    def __unicode__(self):
      return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    description=models.TextField(blank=True, null=True)
    url = models.URLField()
    views = models.IntegerField(default=0)
    def __unicode__(self):
       return self.title

class UserProfile(models.Model):
	user=models.ForeignKey(User, unique=True)
        bio=models.TextField(blank=True)
        location = models.CharField(max_length=128, blank=True)
        birthday=models.DateField(blank=True, null=True)
        website = models.URLField(blank=True, null=True)
	picture = models.ImageField(upload_to='media', blank=True)
        def __unicode__(self):
          return self.user.username
	
