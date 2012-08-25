from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from .articles.models import Article
from .articles.views import Search

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.date_based.archive_index', dict(
            queryset = Article.objects.all(),
            date_field = 'created',
        ), name='home'),
    url(r'^(?P<object_id>\d+)$', 'django.views.generic.list_detail.object_detail', dict(
            queryset = Article.objects.all(),
        ), name='article'),
    url(r'^create$', 'django.views.generic.create_update.create_object', dict(
            model = Article,
        ), name='create_article'),
    url(r'^(?P<object_id>\d+)/edit$', 'django.views.generic.create_update.update_object', dict(
            model = Article,
        ), name='edit_article'),
    url(r'^search$', Search.as_view(), name='search'),


    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
