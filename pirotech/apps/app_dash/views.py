from django.shortcuts import render , HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'app_dash/graficos.html')

@login_required
def estoque(request):
    return render(request, 'app_dash/estoque.html')

@login_required
def funcionario(request):
    return render(request ,'app_dash/funcionario.html')

@login_required
def vendas(request):
    return render(request,'app_dash/venda.html')