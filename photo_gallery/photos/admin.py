import copy
from django.contrib import admin
from .models import Collection, Country, Photo


class CollectionAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'slug', 'photo_count', 'published']
    readonly_fields = ['photo_count']
    list_display = ('name', 'slug', 'photo_count', 'published')

    # Generate a suggested slug from the name in the "add" form
    prepopulated_fields = {"slug": ("name",)}

    def photo_count(self, obj):
        """Return the number of `Photo` objects associated with each `Collection`."""
        return Photo.objects.filter(collections__in=[obj]).count()


class CountryAdmin(admin.ModelAdmin):
    fields = ['name', 'photo_count']
    readonly_fields = ['photo_count']
    list_display = ('name', 'photo_count')

    def photo_count(self, obj):
        """Return the number of `Photo` objects associated with each `Country`."""
        return Photo.objects.filter(country=obj, country__isnull=False).count()


class PhotoAdmin(admin.ModelAdmin):
    fields = ['large_image', 'thumbnail_img_tag', 'title', 'slug', 'description', 'location',
              'country', 'date_taken', 'collections', 'featured', 'published']

    # Generate a suggested slug from the title in the "add" form
    prepopulated_fields = {"slug": ("title",)}

    # Display a non-editable thumbnail on Photo change pages
    readonly_fields = ['thumbnail_img_tag']

    # Use JS filter interface for selecting collections
    filter_horizontal = ('collections',)

    list_display = ('title', 'thumbnail_img_tag', 'slug', 'published')
    list_display_links = ('title', 'thumbnail_img_tag')
    list_filter = ['date_taken', 'featured', 'collections', 'country']
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


admin.site.register(Collection, CollectionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Photo, PhotoAdmin)
