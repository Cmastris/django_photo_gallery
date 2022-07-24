from django.contrib import admin
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    # TODO: add photo upload text (at least 2000px wide, otherwise low visual quality)
    # TODO: improve admin appearance
    pass


admin.site.register(Photo, PhotoAdmin)
