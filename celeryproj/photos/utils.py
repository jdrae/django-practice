import json

import requests

from . import settings as photo_settings
from .models import Photo


def get_latest_flick_image():
    url = photo_settings.FLICKR_JSON_FEED_URL
    req = requests.get(url)
    page_content = req.text

    probably_json = page_content.replace("\\'", "'")
    feed = json.loads(probably_json)
    images = feed['items']
    return images[0]


def save_latest_flickr_image():
    flickr_image = get_latest_flick_image()
    if not Photo.objects.filter(link=flickr_image['link']).exists(): # 중복된것 방지
        photo = Photo(
            title=flickr_image['title'],
            link=flickr_image['link'],
            image_url=flickr_image['media']['m'],
            description=flickr_image['description']
        )
        photo.save()
