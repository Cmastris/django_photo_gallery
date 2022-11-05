from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from photos.models import Collection, Photo


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return ['homepage', 'contact']

    def location(self, item):
        return reverse(item)


class CollectionSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Collection.objects.filter(published=True)


class PhotoSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Photo.objects.filter(published=True).order_by('-date_taken')

    def lastmod(self, photo):
        return photo.last_modified
