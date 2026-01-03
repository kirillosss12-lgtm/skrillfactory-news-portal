
from django.urls import path
from news.views import index, news, news_detail

app_name='news'

urlpatterns = [
    path('', index, name='index'),
    path('news/', news, name='news'),
    path('news/<int:pk>/', news_detail, name='news_detail')

]
