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
from django.urls import path
from django.views.defaults import page_not_found

from photos.views import PhotoDetailView, PhotoListView


def custom_404_template(request):
    return page_not_found(request, None)


urlpatterns = [
    path('', PhotoListView.as_view(), name='homepage'),
    path('admin/', admin.site.urls),
    path('photos/<slug:slug>', PhotoDetailView.as_view(), name='photo_detail'),
    path('404', custom_404_template),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# https://docs.djangoproject.com/en/4.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
