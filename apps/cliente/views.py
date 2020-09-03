from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from .forms import ClienteForm, SetPasswordForm
from .models import Cliente


@login_required
@user_passes_test(lambda u: u.is_superuser)
def create(request):
    form = ClienteForm()
    password_form = SetPasswordForm()
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        password_form = SetPasswordForm(request.POST)
        if form.is_valid() and password_form.is_valid():
            cliente = form.save()
            cliente.set_password(password_form.cleaned_data.get('password1'))
            cliente.save()
            messages.success(request, "Cliente criado com sucesso!")
            return redirect('cliente:create')

    clientes = Cliente.objects.filter(is_active=True)
    context = {
        'form': form,
        'password_form': password_form,
        'clientes': clientes
    }
    return render(request, "cliente/create.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def update(request, pk):
    instance = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(instance=instance)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente alterado com sucesso!")
            return redirect('cliente:create')

    context = {
        'form': form,
        'pk': pk
    }
    return render(request, "cliente/update.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def set_password(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
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
        return redirect('cliente:create')

    context = {
        'form': form,
        'pk': pk
    }
    return render(request, "cliente/set_password.html", context)


def delete(request, pk):
    try:
        cliente = get_object_or_404(Cliente, pk=pk)
        # cliente.delete()
        messages.success(request, "Cliente removido com sucesso!")
    except Exception as exc:
        messages.error(request, "Erro ao remover cliente!")

    return JsonResponse({'result': 'success'})
