from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def create(request):
    return render(request, 'location/list.html')
