from django.urls import path
from .import views

app_name = "leitos"

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    # APIs integradas (inclui funcionalidades do main.py)
    path("api/zona_leitos/", views.api_zona_leitos, name="api_zona_leitos"),
    path("api/zona_especialidades/", views.api_zona_especialidades, name="api_zona_especialidades"),
    path("api/evolucao_leitos/", views.api_evolucao_leitos, name="api_evolucao_leitos"),
    path("api/taxa_ocupacao_sus/", views.api_taxa_ocupacao_sus, name="api_taxa_ocupacao_sus"),
    path("api/estabelecimentos/", views.api_estabelecimentos_table, name="api_estabelecimentos"),
    path("api/estabelecimentos/export/", views.api_estabelecimentos_export_csv, name="api_estabelecimentos_export"),
    path("api/por_municipio/<str:municipio>/", views.api_por_municipio, name="api_por_municipio"),
    path("api/por_zona/<str:zona>/", views.api_por_zona, name="api_por_zona"),
    path("api/por_cep/<str:cep>/", views.api_por_cep, name="api_por_cep"),
    path("api/filters/", views.api_filters, name="api_filters"),
]
