from django.urls import path
from . import views

app_name = 'flashcard'

urlpatterns = [
    path('novo-flashcard/', views.novo_flashcard,
         name='novo_flashcard'),
    path('deletar-flashcard/<int:flashcard_id>/',
         views.deletar_flashcard, name='deletar_flashcard'),
    path('iniciar-desafio/', views.iniciar_desafio,
         name='iniciar_desafio'),
    path('listar-desafio/', views.listar_desafio, name='listar_desafio'),
    path('desafio/<int:desafio_id>/', views.desafio,
         name='desafio'),
    path('responder-flashcard/<int:id>/',
         views.responder_flashcard, name='responder_flashcard'),
    path('relatorio/<int:desafio_id>/', views.relatorio, name='relatorio'),
]
