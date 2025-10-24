from django import forms
from .models import Produto, Venda , Despesa

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'tipo_animal', 'tipo', 'peso', 'quantidade']
        labels = {
            'nome': 'Nome do Comprador',
            'tipo_animal': 'Animal',
            'tipo': 'Tipo de Ração',
            'peso': 'Peso do Saco',
            'quantidade': 'Quantidade em Estoque'
        }


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['produto', 'quantidade_vendida']
        labels = {
            'produto': 'Selecione o Produto',
            'quantidade_vendida': 'Quantidade Vendida'
        }

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['valor']
        widgets = {
            'valor': forms.NumberInput(attrs={'placeholder':'Digite o valor das despesas em R$'})

        }