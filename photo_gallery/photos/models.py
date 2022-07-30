from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.db import models
from django.utils.html import mark_safe
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit


def validate_lowercase(string):
    # https://docs.djangoproject.com/en/4.0/ref/validators/
    lower_str = string.lower()
    if string != lower_str:
        raise ValidationError("All letters must be lowercase.")


class Photo(models.Model):
    # TODO: slug, description, country, date, featured, collections (0+)
    img_guidelines = "Upload images with a width of 2000px or greater " \
                     "to avoid low visual quality (e.g. pixelation) on larger screen sizes."

    # https://django-imagekit.readthedocs.io/en/latest/#defining-specs-in-models
    # Avoid storing and serving very large uploaded image files
    large_image = ProcessedImageField(verbose_name="image file",
                                      help_text=img_guidelines,
                                      processors=[ResizeToFit(width=2000)],
                                      format='JPEG',
                                      options={'quality': 80})

    # Use to improve loading performance (photo listings and mobile images)
    small_image = ImageSpecField(source='large_image',
                                 processors=[ResizeToFit(width=500)],
                                 format='JPEG')

    # Display in the admin interface via `thumbnail_img_tag()`
    thumbnail = ImageSpecField(source='large_image',
                               processors=[ResizeToFit(width=250)],
                               format='JPEG')

    @admin.display(description='Thumbnail')
    def thumbnail_img_tag(self):
        return mark_safe('<img src="{}" />'.format(self.thumbnail.url))

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


# TODO: Collection with name (unique), description, slug (unique)
# https://docs.djangoproject.com/en/4.0/ref/models/fields/#unique
