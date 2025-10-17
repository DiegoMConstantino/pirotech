from django.urls import path
from . import views

urlpatterns = [
    path('',views.entrar , name="entrar"),
    path('dono/',views.pagina_dono , name="pagina_dono"),
    path('gerente/',views.pagina_gerente, name="pagina_gerente"),
    path('funcionario/',views.pagina_funcionario , name="pagina_funcionario"),
]