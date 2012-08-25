from haystack import indexes, site
from .models import Article

class ArticleIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    created = indexes.DateTimeField(model_attr='created')
    modified = indexes.DateTimeField(model_attr='modified')
    get_absolute_url = indexes.CharField(model_attr='get_absolute_url')

    def prepare_text(self, obj):
        return '\n'.join([obj.title, obj.description])

site.register(Article, ArticleIndex)
