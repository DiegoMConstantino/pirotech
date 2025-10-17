from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# Helper functions for role-based access checks
def is_dono(user ):
    return user.is_authenticated and user.is_dono

def is_gerente(user):
    return user.is_authenticated and user.is_gerente

def is_funcionario(user):
    return user.is_authenticated and user.is_funcionario

# Decorator for Dono access
def dono_required(function=None, redirect_field_name=None, login_url='entrar'):
    actual_decorator = user_passes_test(
        is_dono,
        redirect_field_name=redirect_field_name,
        login_url=login_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# Decorator for Gerente access
def gerente_required(function=None, redirect_field_name=None, login_url='entrar'):
    actual_decorator = user_passes_test(
        is_gerente,
        redirect_field_name=redirect_field_name,
        login_url=login_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# Decorator for Funcionario access
def funcionario_required(function=None, redirect_field_name=None, login_url='entrar'):
    actual_decorator = user_passes_test(
        is_funcionario,
        redirect_field_name=redirect_field_name,
        login_url=login_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# Create your views here.
def entrar(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        user = authenticate(request, email=email, password=senha)
        
        if user is not None:
            login(request, user)

            # Redirect based on role after successful login
            if user.is_dono:
                return redirect('pagina_dono')
            elif user.is_gerente:
                return redirect('pagina_gerente')
            else:
                return redirect('pagina_funcionario')
        else:
            messages.error(request, "Email ou senha inválidos.") # More generic message
    return render(request, "app_cadastro/entrar.html")

@login_required(login_url='entrar')
@dono_required
def pagina_dono(request):
    # The role check is now handled by the @dono_required decorator
    return render(request, 'app_dash/pagina_dono.html')

@login_required(login_url='entrar')
@gerente_required
def pagina_gerente(request):
    # The role check is now handled by the @gerente_required decorator
    return render(request, 'app_dash/pagina_gerente.html')

@login_required(login_url='entrar')
@funcionario_required
def pagina_funcionario(request):
    # The role check is now handled by the @funcionario_required decorator
    return render(request, 'app_dash/pagina_funcionario.html')
