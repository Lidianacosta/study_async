from django.contrib import admin
from . import models

# Register your models here


class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('id', 'pergunta', 'dificuldade', 'categoria', 'user')
    list_display_links = ('id', 'pergunta', 'user')


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')


class FlashcardDesafioAdmin(admin.ModelAdmin):
    list_display = ('id', 'flashcard', 'respondido', 'acertou')
    list_display_links = ('id', 'flashcard')
    readonly_fields = ('respondido', 'acertou')


class DesafioAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'titulo', 'quantidade_perguntas', 'dificuldade', 'user'
    )
    list_display_links = (
        'id', 'titulo', 'quantidade_perguntas', 'dificuldade', 'user'
    )

    filter_horizontal = ('categoria', 'flashcards')


admin.site.register(models.Flashcard, FlashcardAdmin)
admin.site.register(models.Categoria, CategoriaAdmin)
admin.site.register(models.Desafio, DesafioAdmin)
admin.site.register(models.FlashcardDesafio, FlashcardDesafioAdmin)
