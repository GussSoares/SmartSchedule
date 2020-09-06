from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as django_login, logout as django_logout, update_session_auth_hash
from django.contrib import messages
from .forms import LoginForm, RegisterForm
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
    register_form = RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            cliente = register_form.save()
            cliente.set_password(register_form.cleaned_data.get('password1'))
            cliente.save()
            django_login(request, cliente)
            return redirect('dashboard:index')

    context = {
        'register_form': register_form
    }
    return render(request, 'register/register.html', context)


def profile(request):

    instance = get_object_or_404(Cliente, pk=request.user.id)
    form = ClienteForm(instance=instance)
    password_form = SetPasswordForm()

    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=instance)
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
        'profile': instance,
        'password_form': password_form
    }
    return render(request, 'profile/profile.html', context)
