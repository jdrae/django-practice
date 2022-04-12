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