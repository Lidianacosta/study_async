from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import Http404
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
# Create your views here.


def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')

    if request.method == 'GET':
        categorias = Categoria.objects.all().order_by('nome')
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user)

        categoria = request.GET.get('categoria')
        dificuldade = request.GET.get('dificuldade')

        if categoria:
            flashcards = flashcards.filter(categoria__id=categoria)
        if dificuldade:
            flashcards = flashcards.filter(dificuldade=dificuldade)

        context = {
            'categorias': categorias,
            'dificuldades': dificuldades,
            'flashcards': flashcards,
        }
        return render(request, 'flashcard/novo_flashcard.html', context)
    if request.method == 'POST':
        pergunta = request.POST.get('pergunta').strip()
        resposta = request.POST.get('resposta').strip()
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if not len(pergunta) or not len(resposta):
            messages.error(
                request, 'Os campos pergunta e resposta precisam ser preenchidos')
            return redirect('flashcard:novo_flashcard')

        flashcard = Flashcard(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade,
        )
        flashcard.save()
        messages.success(request, 'Flashcard cadastrado com sucessso')
        return redirect('flashcard:novo_flashcard')


def deletar_flashcard(request, flashcard_id):
    flashcard = Flashcard.objects.get(pk=flashcard_id)
    if not flashcard.user == request.user:
        messages.error(request, 'Você só pode apagar os seus flashcards')
        return redirect(reverse('flashcard:novo_flashcard'))

    flashcard.delete()
    messages.success(request, 'Flashcard deletado com sucesso!')
    return redirect(reverse('flashcard:novo_flashcard'))


def iniciar_desafio(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all().order_by('nome')
        dificuldades = Flashcard.DIFICULDADE_CHOICES

        context = {
            'categorias': categorias,
            'dificuldades': dificuldades,
        }
        return render(request, 'flashcard/iniciar_desafio.html', context)

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = int(request.POST.get('qtd_perguntas'))

        if qtd_perguntas <= 0:
            messages.error(request, 'Quantidade de perguntas inválida')
            return redirect(reverse('flashcard:iniciar_desafio'))

        flashcards = (
            Flashcard.objects.filter(user=request.user)
            .filter(dificuldade=dificuldade)
            .filter(categoria_id__in=categorias)
            .order_by('?')
        )

        flashcards_quantidades = flashcards.count()

        if flashcards_quantidades < qtd_perguntas:
            qtd_perguntas = flashcards_quantidades
            messages.warning(
                request,
                'Quantidade de perguntas insuficientes '
                f'foram adicionadas {flashcards_quantidades} perguntas'
            )

        desafio = Desafio(
            user=request.user,
            titulo=titulo,
            quantidade_perguntas=qtd_perguntas,
            dificuldade=dificuldade,
        )
        desafio.save()

        desafio.categoria.add(*categorias)

        flashcards = flashcards[:qtd_perguntas]

        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(flashcard=f)
            flashcard_desafio.save()
            desafio.flashcards.add(flashcard_desafio)

        desafio.save()
        return redirect(reverse('flashcard:listar_desafio'))


def listar_desafio(request):
    if not request.user.is_authenticated:
        return redirect(reverse('usuarios:login'))

    desafios = Desafio.objects.filter(user=request.user)

    dificuldade = request.GET.get('dificuldade')
    categoria = request.GET.get('categoria')

    if categoria:
        desafios = desafios.filter(categoria__id=categoria)

    if dificuldade:
        desafios = desafios.filter(dificuldade=dificuldade)

    context = {
        'desafios': desafios,
        'dificuldades': Flashcard.DIFICULDADE_CHOICES,
        'categorias': Categoria.objects.all(),
    }
    return render(request, 'flashcard/listar_desafio.html', context)


def desafio(request, desafio_id):
    if request.method == 'GET':
        desafio = Desafio.objects.get(pk=desafio_id)

        if not request.user == desafio.user:
            raise Http404()

        acertos = (
            desafio.flashcards.filter(respondido=True)
            .filter(acertou=True).count()
        )
        erros = (
            desafio.flashcards.filter(respondido=True)
            .filter(acertou=False).count()
        )
        faltantes = desafio.flashcards.filter(respondido=False).count()

        context = {
            'desafio': desafio,
            'acertos': acertos,
            'erros': erros,
            'faltantes': faltantes,
        }

        return render(
            request, 'flashcard/desafio.html', context
        )


def responder_flashcard(request, id):
    flashcard_desafio = FlashcardDesafio.objects.get(pk=id)
    resposta = request.GET.get('acertou')
    desafio_id = request.GET.get('desafio_id')

    if not flashcard_desafio.flashcard.user == request.user:
        raise Http404()

    # http_referer = request.META.get('HTTP_REFERER')
    flashcard_desafio.acertou = True if resposta == '1' else False
    flashcard_desafio.respondido = True
    flashcard_desafio.save()

    # return redirect(http_referer)
    return redirect(reverse('flashcard:desafio', args=[desafio_id]))
