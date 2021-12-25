from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .forms import ClientForm, SetPasswordForm, GroupForm, CoordForm, MemberForm
from .models import Client, Coordinator, Member, Group
from ..core.utils import get_subdomain
from ..notification.models import Commentary
import re

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_cliente(request):
    form = ClientForm()
    password_form = SetPasswordForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        password_form = SetPasswordForm(request.POST)
        if form.is_valid() and password_form.is_valid():
            cliente = form.save()
            cliente.set_password(password_form.cleaned_data.get('password1'))
            cliente.save()
            messages.success(request, "Cliente criado com sucesso!")
            return redirect('client:create_client')

    clientes = Client.objects.filter(is_active=True)
    context = {
        'form': form,
        'password_form': password_form,
        'clientes': clientes
    }
    return render(request, "cliente/create.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_cliente(request, pk):
    instance = get_object_or_404(Client, pk=pk)
    form = ClientForm(instance=instance)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente alterado com sucesso!")
            return redirect('client:create_client')

    context = {
        'form': form,
        'pk': pk
    }
    return render(request, "cliente/update.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def set_password(request, pk):
    cliente = get_object_or_404(Client, pk=pk)
    form = SetPasswordForm()

    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            cliente.set_password(form.cleaned_data.get('password1'))
            cliente.save()
            if request.user == cliente:
                update_session_auth_hash(request, cliente)

            messages.success(request, "Senha alterado com sucesso!")
        else:
            messages.error(request, form.errors.as_ul())
        return redirect('client:create_client')

    context = {
        'form': form,
        'pk': pk
    }
    return render(request, "cliente/set_password.html", context)


def delete_cliente(request, pk):
    try:
        cliente = get_object_or_404(Client, pk=pk)
        cliente.delete()
        messages.success(request, "Cliente removido com sucesso!")
    except Exception as exc:
        messages.error(request, "Erro ao remover cliente!")

    return JsonResponse({'result': 'success'})


# ---------------------- COORDENADOR ---------------------- #
@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_coord(request):
    form = ClientForm()
    form_coord = CoordForm()
    password_form = SetPasswordForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        form_coord = CoordForm(request.POST)
        password_form = SetPasswordForm(request.POST)
        if form.is_valid() and password_form.is_valid() and form_coord.is_valid():
            cliente = form.save()
            cliente.set_password(password_form.cleaned_data.get('password1'))
            cliente.save()
            Coordinator.objects.create(cliente=cliente, grupo=form_coord.cleaned_data.get('grupo'))
            messages.success(request, "Coordenador criado com sucesso!")
            return redirect('coordinator:create_coord')

    coords = Coordinator.objects.filter(cliente__is_active=True)
    context = {
        'form': form,
        'form_coord': form_coord,
        'password_form': password_form,
        'coords': coords
    }
    return render(request, 'coordenador/create.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_coord(request, pk):
    instance = get_object_or_404(Coordinator, pk=pk)
    form = ClientForm(instance=instance.cliente)
    form_coord = CoordForm(instance=instance)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=instance.cliente)
        form_coord = CoordForm(request.POST, instance=instance)
        if form.is_valid() and form_coord.is_valid():
            form.save()
            instance.grupo = form_coord.cleaned_data.get('grupo')
            instance.save()
            messages.success(request, "Coordenador alterado com sucesso!")
            return redirect('coordinator:create_coord')

    context = {
        'form': form,
        'form_coord': form_coord,
        'pk': pk
    }
    return render(request, "coordenador/update.html", context)


def delete_coord(request, pk):
    try:
        cliente = get_object_or_404(Client, pk=pk)
        cliente.delete()
        messages.success(request, "Coordenador removido com sucesso!")
    except Exception as exc:
        messages.error(request, "Erro ao remover coordenador!")

    return JsonResponse({'result': 'success'})


# ---------------------- MEMBRO ---------------------- #
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_coordinator)
def list_membro(request):
    form = ClientForm()
    form_member = MemberForm(user=request.user)
    members = Member.objects.filter(cliente__is_active=True)
    if request.user.is_coordinator:
        members = members.filter(Q(grupo__coordinator__cliente=request.user) | Q(grupo=None))

    context = {
        'form': form,
        'form_member': form_member,
        'members': members
    }
    return render(request, 'membro/create.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_coordinator)
def create_membro(request):
    form = ClientForm()
    form_member = MemberForm(user=request.user)
    if request.method == 'POST':
        form = ClientForm(request.POST)
        form_member = MemberForm(request.POST)
        if form.is_valid() and form_member.is_valid():
            cliente = form.save(commit=False)
            cliente.telefone = re.sub(r'\D', '', cliente.telefone)
            cliente.cpf_cnpj = re.sub(r'\D', '', cliente.cpf_cnpj)
            cliente.save()
            member = Member.objects.create(cliente=cliente, grupo=form_member.cleaned_data.get('grupo'))
            # se usuario for coordenador, o grupo é selecionado automaticamente
            if request.user.is_coordinator:
                grupo = Coordinator.objects.get(cliente=request.user).grupo
                member.grupo = grupo
                member.save()
            messages.success(request, "Membro criado com sucesso!")
            return redirect('member:list_member')

    members = Member.objects.filter(cliente__is_active=True)
    if request.user.is_coordinator:
        members = members.filter(Q(grupo__coordinator__cliente=request.user) | Q(grupo=None))

    context = {
        'form': form,
        'form_member': form_member,
        'members': members
    }
    return render(request, 'membro/modals/create.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_coordinator)
def update_membro(request, pk, comment_id=None):
    instance = get_object_or_404(Member, pk=pk)
    form_member = MemberForm(instance=instance, user=request.user)
    form = ClientForm(instance=instance.cliente)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=instance.cliente)
        form_member = MemberForm(request.POST, instance=instance)
        if form.is_valid() and form_member.is_valid():
            form.save()
            # se o usuario for admnistrador, pode alterar o grupo do membro
            if request.user.is_superuser:
                instance.grupo = form_member.cleaned_data.get('grupo')
                instance.save()
            messages.success(request, "Membro alterado com sucesso!")
            # tenta redirecionar para a pagina que chamou a requisicao.
            # se nao conseguir, por padrao redireciona para tela de membros
            try:
                with transaction.atomic(using=get_subdomain(request)):
                    if comment_id:
                        comment = Commentary.objects.get(id=comment_id)
                        comment.checked = True
                        comment.save()
                return redirect(request.META['HTTP_REFERER'])
            except:
                return redirect('member:create_member')

    context = {
        'form': form,
        'form_member': form_member,
        'pk': pk,
        'comment_id': comment_id
    }
    return render(request, 'membro/update.html', context)


def delete_membro(request, pk):
    try:
        cliente = get_object_or_404(Client, pk=pk)
        cliente.delete()
        messages.success(request, "Membro removido com sucesso!")
    except Exception as exc:
        messages.error(request, "Erro ao remover membro!")

    return JsonResponse({'result': 'success'})


# ---------------------- GRUPO ---------------------- #
@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_grupo(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Grupo criado com sucesso!")
            return redirect('group:create_group')

    groups = Group.objects.all()
    context = {
        'form': form,
        'groups': groups
    }
    return render(request, 'grupo/create.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_grupo(request, pk):
    instance = get_object_or_404(Group, pk=pk)
    form = GroupForm(instance=instance)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Grupo alterado com sucesso!")
            return redirect('group:create_group')

    context = {
        'form': form,
        'pk': pk
    }
    return render(request, 'grupo/update.html', context)


def delete_grupo(request, pk):
    try:
        group = get_object_or_404(Group, pk=pk)
        if Member.objects.filter(grupo=group).exists():
            messages.warning(request, "Existem membros associados a este grupo!")
        elif Coordinator.objects.filter(grupo=group).exists():
            messages.warning(request, "Existem coordenadores associados a este grupo!")
        else:
            group.delete()
            messages.success(request, "Grupo removido com sucesso!")
    except Exception as exc:
        messages.error(request, "Erro ao remover grupo!")
    return JsonResponse({'result': 'success'})

