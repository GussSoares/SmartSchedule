from django.shortcuts import render


def handler_404(request, *args, **kwargs):
    return render(request, 'error/404.html')


def handler_500(request, *args, **kwargs):
    return render(request, 'error/500.html')
