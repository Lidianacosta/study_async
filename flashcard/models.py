from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return str(self.nome)


class Flashcard(models.Model):
    DIFICULDADE_CHOICES = (
        ('F', 'Fácil'), ('M', 'Médio'), ('D', 'Difícil')
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    pergunta = models.CharField(max_length=100)
    resposta = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    dificuldade = models.CharField(
        max_length=1, choices=DIFICULDADE_CHOICES, default='F'
    )

    def __str__(self):
        return str(self.pergunta)
