from django.db import models
from sorl import thumbnail

class Screenshot(models.Model):
    """A screenshot displayed in the media gallery, which can optionally be
    promoted to the homepage"""

    game_name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    image = thumbnail.ImageField(upload_to='screenshots')
    displayed = models.BooleanField(default=True)
    promoted = models.BooleanField(default=False)

    def __str__(self):
        return self.game_name

    def get_absolute_url(self):
        return self.image.url
