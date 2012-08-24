from django.core.urlresolvers import reverse
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel

class Article(TitleSlugDescriptionModel, TimeStampedModel):
    """
    TitleSlugDescriptionModel:
        title = CharField
        slug = AutoSlugField (CharField)
        description = TextField (null=true)

    TimeStampedModel:
        created = DateTimeField
        modified = DateTimeField
    """
    def get_absolute_url(self):
        return reverse('article', kwargs=dict(object_id=self.pk))

    def __unicode__(self):
        return self.title
