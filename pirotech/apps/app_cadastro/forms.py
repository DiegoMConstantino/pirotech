from django import forms
from .models import CustomUser

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['role'].choices = [
            ('GERENTE', 'Gerente'),
            ('FUNCIONARIO', 'Funcionário'),
        ]
        
        self.fields['password'].widget = forms.PasswordInput()

    def save(self, commit=True):
        
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
