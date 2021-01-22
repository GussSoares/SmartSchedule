import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as django_login, logout as django_logout, update_session_auth_hash
from django.contrib import messages
from .forms import LoginForm, RegisterForm, LoginConfirmForm
from ..cliente.forms import ClientForm, SetPasswordForm
from ..cliente.models import Client, Member


def login(request):
    form = LoginForm()
    next = request.GET.get('next')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            user = authenticate(request, login=login, password=password)

            if user:
                django_login(request, user)
                if request.POST.get('next'):
                    return redirect(request.POST.get('next'))
                return redirect('dashboard:index')
            else:
                messages.error(request, "Usuário ou Senha incorretos!")

    context = {
        'form': form,
        'next': next
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
            cliente.is_superuser = True
            cliente.set_password(register_form.cleaned_data.get('password1'))
            cliente.save()
            django_login(request, cliente)
            return redirect('dashboard:index')

    context = {
        'register_form': register_form
    }
    return render(request, 'register/register.html', context)


def profile(request):

    instance = get_object_or_404(Client, pk=request.user.id)
    form = ClientForm(instance=instance)
    password_form = SetPasswordForm()

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=instance)
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


def login_confirm(request):
    form = LoginConfirmForm()
    if request.method == "POST":
        form = LoginConfirmForm(request.POST)
        if form.is_valid():
            try:
                cpf = re.sub(r'\D', '', form.cleaned_data.get('cpf_cnpj'))
                member = Member.objects.get(cliente__cpf_cnpj=cpf)
                return render(request, 'confirm/confirm_notification.html', {'member': member})
            except Exception as exc:
                messages.error(request, 'Cadastro não localizado')
                return redirect('acl:schedule_view')
    return render(request, 'confirm/login_confirm_notification.html', {'form': form})


def confirm(request):
    return render(request, 'confirm/confirm_notification.html')
