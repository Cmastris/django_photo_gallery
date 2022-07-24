from django.contrib import admin
from imagekit.admin import AdminThumbnail
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')


admin.site.register(Photo, PhotoAdmin)
