from django.urls import path
from . import views

app_name = 'apostilas'

urlpatterns = [
    path('adicionar-apostilas/',
         views.adicionar_apostilas, name='adicionar_apostilas'),
    path('apostila/<int:apostila_id>', views.apostila, name='apostila'),
]
