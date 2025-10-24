from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto, Venda ,  Despesa
from .forms import VendaForm, ProdutoForm , DespesaForm
import plotly.express as px
import pandas as pd
import logging
from datetime import datetime

@login_required
def graficos(request):
    meta = None
    percentual = None

    if request.method == 'POST':
        if 'meta_faturamento' in request.POST:
            meta_valor = request.POST.get('meta_faturamento', 0)
            try:
                meta = float(meta_valor)
            except ValueError:
                meta = 0.0
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('graficos')
    else:
        form = DespesaForm()

    hoje = datetime.now()
    mes_atual = hoje.month
    ano_atual = hoje.year
    vendas = Venda.objects.filter(data__month=mes_atual, data__year=ano_atual)
    total_vendas = vendas.count()
    faturamento = float(sum(float(v.total) for v in vendas))
    despesas_mes = Despesa.objects.filter(mes_referencia__month=mes_atual, mes_referencia__year=ano_atual)
    gastos = float(sum(float(d.valor) for d in despesas_mes))
    lucro = faturamento - gastos
    produtos = Produto.objects.all()
    total_estoque = sum(p.quantidade for p in produtos)

    if vendas.exists():
        df_vendas = pd.DataFrame(list(vendas.values('produto__nome', 'produto__tipo_animal', 'quantidade_vendida')))
        agrupado = df_vendas.groupby(['produto__nome', 'produto__tipo_animal'])['quantidade_vendida'].sum().reset_index()
        mais_vendido = agrupado.loc[agrupado['quantidade_vendida'].idxmax()]
        menos_vendido = agrupado.loc[agrupado['quantidade_vendida'].idxmin()]
        produto_mais_vendido = f"{mais_vendido['produto__nome']} ({mais_vendido['produto__tipo_animal']})"
        produto_menos_vendido = f"{menos_vendido['produto__nome']} ({menos_vendido['produto__tipo_animal']})"
    else:
        produto_mais_vendido = produto_menos_vendido = 'Nenhum registro'

    if meta and meta > 0:
        percentual = round((faturamento / meta) * 100, 2)
    else:
        percentual = None

    if vendas.exists():
        df_diario = pd.DataFrame(list(vendas.values('data', 'total')))
        df_diario['data'] = pd.to_datetime(df_diario['data'])
        df_diario['dia'] = df_diario['data'].dt.day  
        df_diario = df_diario.groupby('dia')['total'].sum().reset_index()

        grafico_vendas = px.line(
            df_diario,
            x='dia', y='total',
            title='Faturamento Diário do Mês',
            markers=True,
            line_shape='spline'
        ).to_html(full_html=False)
    else:
        grafico_vendas = "<p>Sem vendas registradas no mês.</p>"

    df_financeiro = pd.DataFrame({
        'Categoria': ['Faturamento', 'Gastos', 'Lucro'],
        'Valor': [faturamento, gastos, lucro]
    })
    grafico_financeiro = px.bar(
        df_financeiro, x='Categoria', y='Valor', color='Categoria',
        title='Resumo Financeiro do Mês'
    ).to_html(full_html=False)

    context = {
        'form': form,
        'total_vendas': total_vendas,
        'faturamento': faturamento,
        'gastos': gastos,
        'lucro': lucro,
        'total_estoque': total_estoque,
        'produto_mais_vendido': produto_mais_vendido,
        'produto_menos_vendido': produto_menos_vendido,
        'grafico_vendas': grafico_vendas,
        'grafico_financeiro': grafico_financeiro,
        'meta': meta,
        'percentual': percentual,
    }

    return render(request, 'app_dash/graficos.html', context)

@login_required
def estoque(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.preco = produto.calcular_preco()
            produto.save()  
            messages.success(request, 'Produto adicionado com sucesso!')
            return redirect('estoque') 
    else:
        form = ProdutoForm()
    
    produtos = Produto.objects.all()
    return render(request, 'app_dash/estoque.html', {'form': form, 'produtos': produtos})

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