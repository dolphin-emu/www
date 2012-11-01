from django.conf import settings
from django.db import models

class NewsArticle(models.Model):
    """A news article which can be linked to a forum post for comments"""

    title = models.CharField(max_length=64)
    slug = models.SlugField()
    author = models.CharField(max_length=64)
    posted_on = models.DateTimeField(auto_now_add=True)
    forum_pid = models.IntegerField(null=True)
    text = models.TextField()
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    @property
    def forum_url(self):
        return settings.FORUM_URL + u'showthread.php?tid=%d' % self.forum_pid

    @models.permalink
    def get_absolute_url(self):
        return ('news-article', [self.slug])
