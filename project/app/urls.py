from . import views
from django.urls import path, include
urlpatterns = [
    path('crawlerresult', views.index),
    path('search/', views.search),
    path('trie', views.trie_search),
    path('articlehome', views.article_home),
    path('articlesearch', views.article_search),
    path('article_search_specific_home', views.article_search_specific_home),
    path('article_search_specific', views.article_search_specific),
    path('projecthome', views.project_search_home),
    path('projectresult',views.project_search),
    path('download_smart_city', views.download_smart_city, name = 'download_smart_city'),
    path('download_smart_transit', views.download_smart_transit, name = 'download_smart_transit'),
    path('', views.home)
    ]
