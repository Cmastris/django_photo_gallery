from django.contrib import admin
from .models import NavSection, NavLink


class NavLinkInline(admin.StackedInline):
    # Display 1 inlined NavLink add form at a time, up to 8
    model = NavLink
    extra = 1
    max_num = 8


class NavSectionAdmin(admin.ModelAdmin):
    inlines = [NavLinkInline]


admin.site.register(NavSection, NavSectionAdmin)
