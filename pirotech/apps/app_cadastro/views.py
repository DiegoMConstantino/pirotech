from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser
from .forms import FuncionarioForm


def is_dono(user):
    return user.is_authenticated and user.is_dono

def is_gerente(user):
    return user.is_authenticated and user.is_gerente

def is_funcionario(user):
    return user.is_authenticated and user.is_funcionario


def dono_required(function=None, redirect_field_name=None, login_url='entrar'):
    actual_decorator = user_passes_test(
        is_dono,
        redirect_field_name=redirect_field_name,
        login_url=login_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def gerente_required(function=None, redirect_field_name=None, login_url='entrar'):
    actual_decorator = user_passes_test(
        is_gerente,
        redirect_field_name=redirect_field_name,
        login_url=login_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def funcionario_required(function=None, redirect_field_name=None, login_url='entrar'):
    actual_decorator = user_passes_test(
        is_funcionario,
        redirect_field_name=redirect_field_name,
        login_url=login_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def entrar(request):
    '''
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        user = authenticate(request, email=email, password=senha)
        
        if user is not None:
            login(request, user)
            if user.is_dono:
                return redirect('pagina_dono')
            elif user.is_gerente:
                return redirect('pagina_gerente')
            else:
                return redirect('pagina_funcionario')
        else:
            messages.error(request, "Email ou senha inválidos.")
            '''
    return render(request, "app_cadastro/entrar.html")


@login_required(login_url='entrar')
@dono_required
def pagina_dono(request):
    return render(request, 'app_dash/pagina_dono.html')

@login_required(login_url='entrar')
@gerente_required
def pagina_gerente(request):
    return render(request, 'app_dash/pagina_gerente.html')

@login_required(login_url='entrar')
@funcionario_required
def pagina_funcionario(request):
    return render(request, 'app_dash/pagina_funcionario.html')


@login_required(login_url='entrar')
@dono_required
def funcionarios_list(request):
   
    print(">>> View FUNCIONARIOS_LIST foi chamada!")

   
    funcionarios = CustomUser.objects.filter(role__in=['GERENTE', 'FUNCIONARIO']).order_by('username')

  
    print(">>> Funcionários encontrados:", list(funcionarios.values('username', 'role')))

    return render(request, 'app_dash/funcionario.html', {
        'funcionarios': funcionarios
    })

@login_required(login_url='entrar')
@dono_required
def funcionario_create(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário/Gerente criado com sucesso!')
            return redirect('funcionario')
    else:
        form = FuncionarioForm()
    return render(request, 'app_dash/funcionario_form.html', {'form': form})


@login_required(login_url='entrar')
@dono_required
def funcionario_delete(request, pk):
    funcionario = get_object_or_404(CustomUser, pk=pk, role__in=['GERENTE', 'FUNCIONARIO', 'gerente', 'funcionario'])
    if request.method == 'POST':
        funcionario.delete()
        messages.success(request, 'Funcionário/Gerente deletado com sucesso!')
        return redirect('funcionario')
    return render(request, 'app_dash/funcionario_confirm_delete.html', {'funcionario': funcionario})


def logout_view(request):
    logout(request)
    messages.success(request,'Logout realizado')
    return redirect('entrar')


def promover_funcionario(request, pk):
    funcionario = get_object_or_404(CustomUser, pk=pk)
    funcionario.role = 'GERENTE'
    funcionario.save()
    messages.success(request, f'{funcionario.username} foi promovido a gerente.')
    return redirect('funcionario')