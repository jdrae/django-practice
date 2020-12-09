import datetime

from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    contents = models.TextField()
    pub_date = models.DateTimeField(auto_now = True)
    views = models.IntegerField(default = 0)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
