from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# --- Carregar os dados ---
df = pd.read_csv("Consolidado_SP.csv", sep=";", encoding="utf-8-sig", dtype=str)

# --- Inicializar o app FastAPI ---
app = FastAPI(title="API de Estabelecimentos de SP", version="1.0")

# --- Configurar CORS (libera acesso do frontend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pode restringir depois ao domínio do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rotas da API ---


@app.get("/")
def home():
    return {"mensagem": "API de Estabelecimentos de SP está online 🚀"}


@app.get("/todos")
def listar_todos(limite: int = Query(20, ge=1, le=500)):
    """Retorna os primeiros registros do arquivo."""
    return df.head(limite).to_dict(orient="records")


@app.get("/zonas")
def listar_zonas():
    """Retorna a contagem de estabelecimentos por zona."""
    zonas = df['ZONA'].value_counts().reset_index()
    zonas.columns = ['zona', 'quantidade']
    return zonas.to_dict(orient="records")


@app.get("/por_zona/{zona}")
def filtrar_por_zona(zona: str):
    """Retorna todos os registros de uma zona específica."""
    zona = zona.strip().title()
    dados = df[df['ZONA'] == zona]
    return dados.to_dict(orient="records")


@app.get("/por_cep/{cep}")
def filtrar_por_cep(cep: str):
    """Busca registros por CEP (parcial ou completo)."""
    cep = cep.replace("-", "")
    dados = df[df['CO_CEP'].str.startswith(cep)]
    return dados.to_dict(orient="records")


@app.get("/por_municipio/{municipio}")
def filtrar_por_municipio(municipio: str):
    """Busca registros por município."""
    municipio = municipio.upper()
    dados = df[df['MUNICIPIO'].str.upper().str.contains(municipio, na=False)]
    return dados.to_dict(orient="records")
