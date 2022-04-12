import os
from celery import Celery
from django.conf import settings

# settings.py 의 환경설정 가져오기
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celeryproj.settings')

app = Celery('celeryproj')
app.config_from_object('django.conf:settings', namespace='CELERY') # 환경설정 적용
app.autodiscover_tasks() #  INSTALLED_APP 에 있는 장고 앱 자동으로 인식

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
