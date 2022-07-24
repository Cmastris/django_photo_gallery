from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit


class Photo(models.Model):
    # TODO: title, slug, description, country, date, featured, collections (0+)
    # https://django-imagekit.readthedocs.io/en/latest/#defining-specs-in-models
    # Avoid storing and serving very large uploaded image files
    large_image = ProcessedImageField(verbose_name="image file",
                                      processors=[ResizeToFit(width=2000)],
                                      format='JPEG',
                                      options={'quality': 80})

    # Use to improve loading performance (photo listings and mobile images)
    small_image = ImageSpecField(source='large_image',
                                 processors=[ResizeToFit(width=500)],
                                 format='JPEG')


# TODO: Collection with name, description, slug
