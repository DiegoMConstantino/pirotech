from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto, Venda
from .forms import VendaForm, ProdutoForm
import plotly.express as px
import pandas as pd
import logging

@login_required
def graficos(request):
    dados = list(Venda.objects.values('data', 'total'))

    if not dados:
        grafico = "<p>Sem dados de vendas para exibir.</p>"
    else:
        
        df = pd.DataFrame(dados)


        df['data'] = pd.to_datetime(df['data']).dt.date


        df_agrupado = df.groupby('data')['total'].sum().reset_index()


        inicio = df_agrupado['data'].min()
        fim = pd.to_datetime('today').normalize().date() + pd.Timedelta(days=1)
        intervalo_completo = pd.date_range(start=inicio, end=fim).date


        df_completo = (
            df_agrupado.set_index('data')
            .reindex(intervalo_completo, fill_value=0)
            .rename_axis('data')
            .reset_index()
        )

      
      
        fig = px.line(
            df_completo,
            x='data',
            y='total',
            title='Total de Dinheiro Ganho por Dia',
            markers=True,
            line_shape='spline'
        )

        fig.update_layout(
            xaxis_title='Data',
            yaxis_title='Total (R$)',
            template='plotly_dark',
            plot_bgcolor="#000000",
            paper_bgcolor='#fff',
            font=dict(family='Arial', size=14)
        )

        grafico = fig.to_html(full_html=False)

    return render(request, 'app_dash/graficos.html', {'grafico': grafico})
@login_required
def estoque(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            

            produto = form.save(commit=False)

           
           
           
        
            produto.preco = produto.calcular_preco()

           
           

            messages.success(request, f'Produto "{produto.nome}" adicionado com preço R$ {produto.preco:.2f}!')
            return redirect('estoque')
        else:

            messages.error(request, 'Houve um erro no formulário. Por favor, verifique os dados.')

    else:
        form = ProdutoForm()

    produtos = Produto.objects.all().order_by('nome') # Ordenar por nome é uma boa prática
    return render(request, 'app_dash/estoque.html', {
        'form': form,
        'produtos': produtos
    })

@login_required
def vendas(request):
    
    
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            produto = venda.produto


            if venda.quantidade_vendida > produto.quantidade:
                messages.error(request, f'Estoque insuficiente! Você só tem {produto.quantidade} unidades.')
            else:

                produto.quantidade -= venda.quantidade_vendida
                produto.save()


                venda.total = venda.quantidade_vendida * produto.preco
                venda.save()

                messages.success(request, f'Venda de {venda.quantidade_vendida}x "{produto.nome}" realizada! Total: R$ {venda.total:.2f}')

                return redirect('vendas')
    else:
        form = VendaForm()

    vendas_list = Venda.objects.all().order_by('-data')
    produtos = Produto.objects.all()
    return render(request, 'app_dash/venda.html', {
        'form': form,
        'produtos': produtos,
        'vendas': vendas_list
    })

@login_required
def dashboard(request):
    return render(request , 'app_dash/graficos.html')