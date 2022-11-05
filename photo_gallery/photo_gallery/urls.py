"""photo_gallery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.defaults import page_not_found
from django.views.generic import TemplateView

from .sitemap_config import CollectionSitemap, PhotoSitemap, StaticViewSitemap
from contact.views import ContactMessageCreateView, ContactSuccessView
from photos.views import CollectionView, PhotoDetailView, PhotoListView, SearchView


def custom_404_template(request):
    return page_not_found(request, None)


urlpatterns = [
    path('', PhotoListView.as_view(), name='homepage'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap,
                                               'collections': CollectionSitemap,
                                               'photos': PhotoSitemap}},
         name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('contact', ContactMessageCreateView.as_view(), name='contact'),
    path('contact-success', ContactSuccessView.as_view(), name='contact_success'),
    path('search', SearchView.as_view(), name='search'),
    path('photos/<slug:slug>', PhotoDetailView.as_view(), name='photo_detail'),
    path('404', custom_404_template),
    path('<slug:collection_slug>', CollectionView.as_view(), name='collection'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# https://docs.djangoproject.com/en/4.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
