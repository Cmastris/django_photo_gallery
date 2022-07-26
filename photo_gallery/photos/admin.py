from django.contrib import admin
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'thumbnail_img_tag')

    # Display a non-editable thumbnail on Photo detail pages
    readonly_fields = ['thumbnail_img_tag']


admin.site.register(Photo, PhotoAdmin)
