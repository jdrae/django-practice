import datetime
from uuid import uuid4
import os

from django.db import models
from django.utils import timezone


def get_file_path(instance, filename):
    ymd = datetime.datetime.now().strftime('%Y%m%d-')
    uuid_name = uuid4().hex
    return 'uploads/' + ymd + uuid_name

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    pub_date = models.DateTimeField(auto_now = True, verbose_name='날짜')
    views = models.IntegerField(default = 0, verbose_name='조회수')
    uploaded_file = models.FileField(upload_to="uploads/", null=True, blank=True, verbose_name='파일')

    def get_file_name(self):
        return os.path.basename(self.uploaded_file.name)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
