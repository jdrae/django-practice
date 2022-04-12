from celery import shared_task
from celery.utils.log import get_task_logger

from feedback.emails import send_feedback_email

logger = get_task_logger(__name__)


# 구체화된 app 인스턴스 없이 task 만들기
# 나머지 프로젝트와 분리되어 있고,
# 항상 현재 실행중인 celery app 을 가르키게 된다
@shared_task(name="send_feedback_email_task")
def send_feedback_email_task(email, message):
    logger.info("Sent feedback email")
    return send_feedback_email(email, message)
