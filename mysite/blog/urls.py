from django.urls import path

from . import views

app_name='blog'
urlpatterns=[
    path('',views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('download/<int:pk>/', views.download_view, name="file_download"),
]