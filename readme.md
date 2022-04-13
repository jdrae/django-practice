# 장고 공부 과정 정리

[명령어 모음](https://github.com/jdrae/django-practice/blob/master/cheatsheet.md)

### 프로젝트 / 앱 설명
* /mysite: **django MTV**
    * /polls [참고링크](https://docs.djangoproject.com/ko/3.1/intro/)

        클래스 뷰 & 테스트 케이스 작성 & 템플릿 활용

    * /blog [참고링크1](https://parkhyeonchae.github.io/2020/04/12/django-project-24/) [참고링크2](https://docs.djangoproject.com/en/3.1/topics/pagination/)

        파일 다운로드 구현 & 페이지네이션

* /restful: **django rest framework**
    * /games [RESTful 파이썬 웹 서비스 제작](http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode=9791161750248)
        
        하이퍼링크시리얼라이저 & 스로틀 & 커스텀 인증 정의

* /celeryproj: **celery**
    * /feedback, /photos [참고링크](https://realpython.com/asynchronous-tasks-with-django-and-celery/#periodic-tasks)

        shared task & periodic task 구현

### 스케줄러와 워커

* celery beat 와 worker 는 독립적이다. 워커 없이 스케줄러가 보내기만 해도 db에 요청이 저장되고, 워커가 켜지는 동시에 요청을 순차적으로 받아서 처리한다. 워커는 요청을 받아서(received) 처리하고(task 실행), 결과를 화면에 표시한다(succeeded in).
* 스케줄러가 연속으로 2개의 태스크를 보내고 워커가 처리하는 과정. 12e79c6d7705, 50a0771df4bd 순으로 도착했지만 50a0771df4bd 가 먼저 완료되는 것을 볼 수 있다.
```
[2022-04-13 12:22:33,254: INFO/MainProcess] Task photos.tasks.task_save_latest_flickr_image[d304c30e-a6ce-4348-beae-12e79c6d7705] received
[2022-04-13 12:22:33,255: INFO/MainProcess] Task photos.tasks.task_save_latest_flickr_image[fc396c08-0bed-4f4b-995b-50a0771df4bd] received
[2022-04-13 12:22:33,766: INFO/ForkPoolWorker-1] photos.tasks.task_save_latest_flickr_image[fc396c08-0bed-4f4b-995b-50a0771df4bd]: Saved image from Flickr
[2022-04-13 12:22:33,773: INFO/ForkPoolWorker-1] Task photos.tasks.task_save_latest_flickr_image[fc396c08-0bed-4f4b-995b-50a0771df4bd] succeeded in 0.5167407280005136s: None
[2022-04-13 12:22:33,774: INFO/ForkPoolWorker-8] photos.tasks.task_save_latest_flickr_image[d304c30e-a6ce-4348-beae-12e79c6d7705]: Saved image from Flickr
[2022-04-13 12:22:33,780: INFO/ForkPoolWorker-8] Task photos.tasks.task_save_latest_flickr_image[d304c30e-a6ce-4348-beae-12e79c6d7705] succeeded in 0.5236574709997512s: None
```

### Redis key 확인

```
127.0.0.1:6379> get "celery-task-meta-c71d9da7-6723-4686-aa23-6d333c54c948"
"{\"status\": \"SUCCESS\", \"result\": null, \"traceback\": null, \"children\": [], \"date_done\": \"2022-04-13T02:59:55.191072\", \"task_id\": \"c71d9da7-6723-4686-aa23-6d333c54c948\"}"
```