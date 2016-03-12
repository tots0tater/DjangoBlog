from datetime import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class BlogPost(models.Model):
    post_title = models.CharField(max_length = 100)
    post_text = models.CharField(max_length = 2000)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.post_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days = 1) <= self.pub_date <= now
    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Comment(models.Model):
    # When a user deletes a blog post, we want to delete
    # all comments that are associated with it.
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length = 2000)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return self.comment_text