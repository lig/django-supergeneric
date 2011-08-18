from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    text = models.TextField()
    
    def __unicode__(self):
        return u'%s: %s' % (self.created, self.title)
    
    class Meta:
        ordering = ['-created']
    
    @models.permalink
    def get_absolute_url(self):
        return ('post', [self.pk])


class Comment(models.Model):
    
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    text = models.TextField()
    
    def __unicode__(self):
        return u'%s: %s' % (self.created, self.text[:255])
    
    class Meta:
        ordering = ['created']
    
    @models.permalink
    def get_absolute_url(self):
        return ('comment', [self.post_id, self.pk])
