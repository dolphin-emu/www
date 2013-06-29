from django.core.urlresolvers import reverse
from django.db import models

class FAQCategory(models.Model):
    """FAQ category and its display order"""

    title = models.CharField(max_length=64)
    slug = models.SlugField()
    display_order = models.IntegerField()

    def sorted_questions(self):
        return self.questions.order_by('display_order')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('docs-faq') + u'#%s' % self.slug

    class Meta:
        verbose_name= "FAQ category"
        verbose_name_plural = "FAQ categories"

class FAQ(models.Model):
    """Describes a frequently asked question"""

    category = models.ForeignKey(FAQCategory, related_name='questions')
    title = models.CharField(max_length=128)
    short_title = models.CharField(max_length=64)
    slug = models.SlugField()
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    text = models.TextField()
    display_order = models.IntegerField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('docs-faq') + u'#%s' % self.slug

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

class Guide(models.Model):
    """A full guide written by a contributor"""

    title = models.CharField(max_length=128)
    slug = models.SlugField()
    wiki_page = models.CharField(max_length=128)
    authors = models.CharField(max_length=128)
    description = models.TextField()
    listed = models.BooleanField(default=False)
    display_order = models.IntegerField()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('docs-guide', [self.slug])

    def get_wiki_url(self):
        return 'https://wiki.dolphin-emu.org/index.php?title=%s&useskin=guideembed' % self.wiki_page

    class Meta:
        db_table = 'docs_guide2'
