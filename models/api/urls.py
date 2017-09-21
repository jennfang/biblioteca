from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^author/(?P<author_id>[0-9]+)$', views.author, name='author'),
    url(r'^author/create$', views.create_author, name='create_author'),
    url(r'^author/delete/(?P<author_id>[0-9]+)$', views.delete_author, name='author'),

    url(r'^book/(?P<book_id>[0-9]+)$', views.book, name='book'),

    url(r'^review/(?P<review_id>[0-9]+)$', views.review, name='review')
]