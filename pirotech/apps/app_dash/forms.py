from django import forms
from .models import Produto, Venda

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
        widgets = {
            'produto': forms.Select(attrs={
                'class': 'nome', 
                'style': 'background-color: #e3b872;'  
            }),
            'quantidade_vendida': forms.NumberInput(attrs={
                'class': 'nome',  
                'style': 'background-color: #e3b872;'
            })
        }