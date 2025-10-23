from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('DONO','Dono'),
        ('GERENTE','Gerente'),
        ('FUNCIONARIO','Funcionario'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES , default='FUNCIONARIO')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_dono(self):
        return self.role == 'DONO'

    @property
    def is_gerente(self):
        return self.role == 'GERENTE'

    @property
    def is_funcionario(self):
        return self.role == 'FUNCIONARIO'
