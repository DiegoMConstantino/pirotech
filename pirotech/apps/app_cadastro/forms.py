from django import forms
from .models import CustomUser

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'func'}),
            'email': forms.EmailInput(attrs={'class': 'func'}),
            'password': forms.PasswordInput(attrs={'class': 'func'}),
            'role': forms.Select(attrs={'class': 'func'}),
        }
        help_texts = {
            'username': ''
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['role'].choices = [
            ('GERENTE', 'Gerente'),
            ('FUNCIONARIO', 'Funcionário'),
        ]
        

    def save(self, commit=True):
        
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    