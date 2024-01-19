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

    @property
    def css_dificuldade(self):
        if self.dificuldade == 'F':
            return 'flashcard-facil'

        if self.dificuldade == 'M':
            return 'flashcard-medio'

        return 'flashcard-dificil'


class FlashcardDesafio(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.DO_NOTHING)
    respondido = models.BooleanField(default=False)
    acertou = models.BooleanField(default=False)

    def __str__(self):
        return str(self.flashcard.pergunta)


class Desafio(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=100)
    categoria = models.ManyToManyField(Categoria)
    quantidade_perguntas = models.IntegerField()
    dificuldade = models.CharField(
        max_length=1, choices=Flashcard.DIFICULDADE_CHOICES
    )
    flashcards = models.ManyToManyField(FlashcardDesafio)

    def __str__(self):
        return str(self.titulo)

    @property
    def status(self):
        respondidas = self.flashcards.all().filter(respondido=True).count()
        if respondidas < self.quantidade_perguntas:
            return 'Pendente'
        return 'Completo'
