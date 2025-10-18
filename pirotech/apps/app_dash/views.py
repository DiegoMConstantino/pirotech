from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'app_dash/dashboard.html')

@login_required
def estoque(request):
    return render(request, 'app_dash/estoque.html')
