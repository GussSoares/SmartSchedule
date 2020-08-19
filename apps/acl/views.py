from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as django_login, logout as django_logout, update_session_auth_hash
from django.contrib import messages
from .forms import LoginForm
from ..cliente.forms import ClienteForm, SetPasswordForm
from ..cliente.models import Cliente


def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            user = authenticate(request, login=login, password=password)

            if user:
                django_login(request, user)

                return redirect('dashboard:index')
            else:
                messages.error(request, "Usuário ou Senha incorretos!")

    context = {
        'form': form
    }
    return render(request, 'login/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('acl:login')


def register(request):
    return render(request, 'register/register.html')


def profile(request):

    instance = get_object_or_404(Cliente, pk=request.user.id)
    form = ClienteForm(instance=instance)
    password_form = SetPasswordForm()

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=instance)
        if form.is_valid():
            user = form.save()
            password_form = SetPasswordForm(request.POST)
            if password_form.changed_data:
                if password_form.is_valid():
                    user.set_password(password_form.cleaned_data.get('password1'))
                    user.save()
                    update_session_auth_hash(request, user)

            messages.success(request, "Dados alterados com sucesso")
            return redirect('acl:profile')

    context = {
        'form': form,
        'password_form': password_form
    }
    return render(request, 'profile/profile.html', context)
