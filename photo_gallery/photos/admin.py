import copy
from django.contrib import admin
from .models import Collection, Country, Photo


class CountryAdmin(admin.ModelAdmin):
    fields = ['name', 'photo_count']
    readonly_fields = ['photo_count']
    list_display = ('name', 'photo_count')

    def photo_count(self, obj):
        """Return the number of `Photo` objects associated with each `Country`."""
        return Photo.objects.filter(country=obj).count()


class PhotoAdmin(admin.ModelAdmin):
    fields = ['large_image', 'thumbnail_img_tag', 'title', 'slug', 'description', 'location',
              'country', 'date_taken']

    # Generate a suggested slug from the title in the "add" form
    prepopulated_fields = {"slug": ("title",)}

    # Display a non-editable thumbnail on Photo change pages
    readonly_fields = ['thumbnail_img_tag']

    list_display = ('title', 'thumbnail_img_tag', 'date_taken', 'slug')
    list_filter = ['date_taken', 'country']
    search_fields = ['title', 'description', 'location']
    search_help_text = "Search photo titles, descriptions, and locations."

    def get_fields(self, request, obj=None):
        """Return a list of fields (str) for the Photo add form (obj=None) or change form.
        https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_fields
        https://github.com/django/django/blob/stable/4.0.x/django/contrib/admin/options.py#L365
        """
        if obj is None:
            # Prevent modification of any lists within `fields`
            add_fields = copy.deepcopy(self.fields)
            # Don't display (non-existent) thumbnail on "add" view
            add_fields.remove('thumbnail_img_tag')
            return add_fields

        return super().get_fields(request, obj)


admin.site.register(Collection)
admin.site.register(Country, CountryAdmin)
admin.site.register(Photo, PhotoAdmin)
