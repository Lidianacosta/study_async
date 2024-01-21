from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tag(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self) -> str:
        return str(self.nome)


class Apostila(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='apostilas')
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return str(self.titulo)


class ViewApostila(models.Model):
    ip = models.GenericIPAddressField()
    apostila = models.ForeignKey(Apostila, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.ip)
