from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Apostila, ViewApostila, Tag
# Create your views here.


def adicionar_apostilas(request):

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        arquivo = request.FILES.get('arquivo')
        tags = request.POST.get('tags')

        if not titulo or not arquivo:
            messages.error(request, 'Os campos precisam está preenchidos')
            return redirect(reverse('apostilas:adicionar_apostilas'))

        apostila = Apostila(
            user=request.user,
            titulo=titulo,
            arquivo=arquivo,
        )
        apostila.save()

        if tags:
            tags = tags.split(',')
            for nome in tags:
                if nome.strip():
                    tag = Tag(nome=nome)
                    tag.save()
                    apostila.tags.add(tag)
            apostila.save()

        messages.success(request, 'Apostila criada com sucesso')
        return redirect(reverse('apostilas:adicionar_apostilas'))

    apostilas = Apostila.objects.filter(user=request.user)

    tag = request.GET.get('tag')
    if tag:
        apostilas = apostilas.filter(tags__nome__icontains=tag)

    views_totais = ViewApostila.objects.filter(
        apostila__user=request.user).count()

    context = {
        "apostilas": apostilas,
        'views_totais': views_totais,
    }
    return render(request, 'apostilas/adicionar_apostilas.html', context)


def apostila(request, apostila_id):
    apostila = Apostila.objects.get(pk=apostila_id)

    views_totais = ViewApostila.objects.filter(apostila=apostila).count()
    views_unicas = ViewApostila.objects.filter(
        apostila=apostila).values('ip').distinct().count()

    view = ViewApostila(
        ip=request.META['REMOTE_ADDR'],
        apostila=apostila,
    )
    view.save()

    context = {
        'apostila': apostila,
        'views_totais': views_totais,
        'views_unicas': views_unicas,
    }
    return render(request, 'apostilas/apostila.html', context)
