### 기본 장고
1. workon myenv
    * pip install virtualenvwrapper
2. django-admin startproject [project name] .
3. django-admin startapp [app name]
4. python manage.py migrate
    * python manage.py check
    * python manage.py sqlmigrate [app name] [migration num]
5. python manage.py createsuperuser --email admin@example.com --username admin
6. python manage.py runserver
    * python manage.py shell


## celery & redis
1. redis-server
2. celery -A [project name] worker -l info
    * celery -A [project name] beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
3. python manage.py runserver

* 2 에서 --scheduler 정의해야 admin page 에서 periodic scheduler 관리 가능
