from django.db import models


class Photo(models.Model):
    # auto_now_add: 처음 만들어진 시각 저장
    # auto_now: save 된 시각 마다 저장
    created_on = models.DateTimeField("Created on", auto_now_add=True)
    updated_on = models.DateTimeField("Updated on", auto_now=True)
    title = models.CharField("Title", max_length=255)
    link = models.URLField("Photo Link", max_length=255, help_text="The URL to the image page")
    image_url = models.URLField("Image URL", max_length=255, help_text="The URL to the image file")
    description = models.TextField("Description")

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"
        ordering = ['-created_on', "title"]

    def __str__(self):
        return self.title
