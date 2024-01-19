from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth
# Create your views here.


def cadastro(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        user = User.objects.filter(username__exact=username)
        if user.exists():
            messages.error(request, 'Usuário já existe')
            return redirect(reverse('usuarios:cadastro'))

        if not senha == confirmar_senha:
            messages.error(request, 'Senha  e confirmar senha não coíncidem')
            return redirect(reverse('usuarios:cadastro'))
        # try:
        User.objects.create_user(
            username=username,
            password=senha
        )
        return redirect(reverse('usuarios:login'))
        # except:
        #     messages.error(request, 'Erro interno do servidor')
        #     return redirect(reverse('usuarios:cadastro'))

    return render(request, 'usuarios/cadastro.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = auth.authenticate(request, username=username, password=senha)
        if user:
            auth.login(request, user)
            messages.success(request, 'Logado!')
            return redirect('flashcard:novo_flashcard')
        messages.error(request, 'username or senha inválido')
    return render(request, 'usuarios/login.html')


def logout(request):
    auth.logout(request)
    return redirect(reverse('usuarios:login'))
