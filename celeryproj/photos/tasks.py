from celery import shared_task
from celery.utils.log import get_task_logger

from photos.utils import save_latest_flickr_image

logger = get_task_logger(__name__)

@shared_task
def task_save_latest_flickr_image():
    save_latest_flickr_image()
    logger.info("Saved image from Flickr")
