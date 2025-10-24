# urls.py

from django.urls import path
from . import views

urlpatterns = [
path('',views.entrar , name="entrar"),
path('logout/', views.logout_view,name='logout'),
path('dono/',views.pagina_dono , name="pagina_dono"),
path('gerente/',views.pagina_gerente, name="pagina_gerente"),
path('funcionario/pagina',views.pagina_funcionario,name="pagina_funcionario"),
path('funcionario/', views.funcionarios_list, name='funcionario'), 
path('funcionarios/criar/', views.funcionario_create, name='funcionario_create'),
path('funcionarios/deletar/<int:pk>/', views.funcionario_delete, name='funcionario_delete'),
path('promover/<int:pk>/', views.promover_funcionario, name='promover_funcionario'),
]


