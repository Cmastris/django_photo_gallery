from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, validate_slug
from django.db import models
from django.utils.html import mark_safe
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit


def validate_lowercase(string):
    # https://docs.djangoproject.com/en/4.0/ref/validators/
    lower_str = string.lower()
    if string != lower_str:
        raise ValidationError("All letters must be lowercase.")


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True, validators=[MinLengthValidator(2)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "countries"


class Photo(models.Model):
    # TODO: date, featured, collections (many to many), published
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

    slug_guidelines = "Enter a unique, descriptive URL path (e.g. based on the title) containing " \
                      "only lowercase letters, numbers,  and hyphens (instead of spaces). "

    slug = models.SlugField(max_length=60,
                            unique=True,
                            help_text=slug_guidelines,
                            validators=[validate_slug, validate_lowercase])

    description = models.TextField(max_length=5000)

    loc_guidelines = "Enter the specific location where the photo was taken."
    location = models.CharField(max_length=255, help_text=loc_guidelines)

    # Country is optional
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{} ({})".format(self.title, self.slug)


# TODO: Collection with name (unique), description, slug (unique), published
