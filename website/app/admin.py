from django.contrib import admin
from .models import *

# Register your models here.


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'nick', 'time_create', 'image')
    list_display_links = ('id', 'nick')
    search_fields = ('nick', 'content')
    prepopulated_fields = {"slug": ("nick",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(User)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Category, CategoryAdmin)
