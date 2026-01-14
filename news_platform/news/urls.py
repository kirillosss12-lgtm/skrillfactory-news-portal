
from django.urls import path
from news.views import index, ProductsList, TovarDetailView, Searh , NewsCreate,NewsUpdate,NewsDelete,ArticleCreate,ArticleUpdate,ArticleDelete

app_name='news'

urlpatterns = [
    path('', index, name='index'),
    path('news/', ProductsList.as_view(), name='news'),
    path('news/<int:pk>/', TovarDetailView.as_view(), name='news_detail'),
    path('news/search/', Searh.as_view(),  name='news_search'),

    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    # Пути для статей
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),

]
