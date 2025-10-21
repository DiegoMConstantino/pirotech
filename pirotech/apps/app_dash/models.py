# models.py

from django.db import models
from django.utils import timezone

class Produto(models.Model):
    """
    Representa um produto no estoque. O preço é o valor de venda unitário.
    A quantidade representa o total de unidades disponíveis em estoque.
    """
    ANIMAIS = [
        ('Cavalo', 'Cavalo'),
        ('Bovino', 'Bovino'),
        ('Ovelha', 'Ovelha'),
        ('Porco', 'Porco'),
        ('Galinha', 'Galinha'),
    ]

    TIPOS = [('Normal', 'Normal'), ('Premium', 'Premium')]

    PESOS = [
        ('500g', '500g'), ('1kg', '1kg'), ('2kg', '2kg'),
        ('5kg', '5kg'), ('10kg', '10kg'), ('20kg', '20kg'),
        ('25kg', '25kg')
    ]

    nome = models.CharField(max_length=100)
    tipo_animal = models.CharField(max_length=50, choices=ANIMAIS, default='Cavalo')
    tipo = models.CharField(max_length=50, choices=TIPOS)
    peso = models.CharField(max_length=20, choices=PESOS)
    quantidade = models.PositiveIntegerField(default=0, verbose_name="Quantidade em Estoque")
    preco = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Preço Unitário (R$)")

    def calcular_preco(self):
        
        
        tabela_precos = {
            'Cavalo': {
                'Premium': {'5kg': 80, '20kg': 280},
                'Normal': {'5kg': 60, '20kg': 200}
            },
            'Bovino': {
                'Premium': {'10kg': 120, '25kg': 280},
                'Normal': {'10kg': 90, '25kg': 200}
            },
            'Ovelha': {
                'Premium': {'2kg': 25, '5kg': 55},
                'Normal': {'2kg': 18, '5kg': 40}
            },
            'Porco': {
                'Premium': {'1kg': 12, '5kg': 55},
                'Normal': {'1kg': 8, '5kg': 40}
            },
            'Galinha': {
                'Premium': {'500g': 10, '1kg': 18},
                'Normal': {'500g': 7, '1kg': 14}
            }
        }
        return tabela_precos.get(self.tipo_animal, {}).get(self.tipo, {}).get(self.peso, 0)

    def __str__(self):
        
        
        return f"{self.nome} ({self.peso}, {self.tipo}) - R$ {self.preco} | Estoque: {self.quantidade}"


class Venda(models.Model):
   
   
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_vendida = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        
        
        return f"Venda de {self.quantidade_vendida}x {self.produto.nome} em {self.data.strftime('%d/%m/%Y')} - Total: R$ {self.total}"

