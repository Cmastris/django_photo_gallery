from django.contrib import admin
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    # TODO: improve admin appearance
    pass


admin.site.register(Photo, PhotoAdmin)
