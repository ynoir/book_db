from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.books, name='books'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>/', views.author, name='author'),
    path('tags/', views.tags, name='tags'),
    path('tags/<int:tag_id>/', views.tag, name='tag'),
    path('statuss/', views.statuss, name='statuss'),
    path('statuss/<int:status_id>/', views.status, name='status'),
]
