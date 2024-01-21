from django.contrib import admin
from .models import Apostila, ViewApostila, Tag

# Register your models here.


@admin.register(Apostila)
class ApostilaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'user')
    list_display_links = ('id', 'titulo', 'user')
    filter_horizontal = ('tags',)


@admin.register(ViewApostila)
class ViewApostilaAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'apostila')
    list_display_links = ('id', 'ip')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')
