from django.db import models

class Screenshot(models.Model):
    """A screenshot that is displayed on the homepage"""

    game_name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='homepage/screenshots')

    def __unicode__(self):
        return self.game_name

    def get_absolute_url(self):
        return self.image.url

class NewsArticle(models.Model):
    """A news article which can be linked to a forum post for comments"""

    title = models.CharField(max_length=64)
    slug = models.SlugField()
    author = models.CharField(max_length=64)
    posted_on = models.DateTimeField(auto_now_add=True)
    forum_pid = models.IntegerField(null=True)
    text = models.TextField()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('news-article', [self.slug])
