# Projeto Integrador IV - Dashboard de Leitos Hospitalares de São Paulo

Este projeto foi desenvolvido utilizando o framework Django.

O conjunto de dashboards tem como objetivo monitorar, analisar e comparar a disponibilidade e ocupação de leitos hospitalares no município de São Paulo, com foco especial nos leitos do Sistema Único de Saúde (SUS).

As visualizações permitem o acompanhamento dinâmico e filtrável por CEP e Zona, facilitando a gestão regionalizada da rede hospitalar.

Ele inclui:

- Gráficos interativos usando **Plotly.js**.
- Filtros por região ou CEP ou ambos.
- Exportação de dados em CSV.
- Tabela paginada de hospitais.


## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

- **Python 3.11+**  
- **pip** (gerenciador de pacotes do Python)  
- **Virtualenv** (opcional, mas recomendado)  
- **PyCharm** (Community ou Professional)


## Configuração do ambiente

1. Clone o repositório ou copie os arquivos do projeto para sua máquina:

```bash
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>
```

2. Crie e ative um ambiente virtual (recomendado):

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / MacOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

> O `requirements.txt` deve conter pelo menos:
```bash
> Django>=4.2
> pandas>=2.1
> plotly>=6.0
> nbformat>=5.0
> nbconvert>=7.0
> jupyter
> numpy
> gunicorn
> ```

4. Execute as migrações do Django:

```bash
python manage.py migrate
```

---

## Rodando o projeto no PyCharm

1. Abra o PyCharm e carregue a pasta do projeto.
2. Configure o **interpreter** para o ambiente virtual criado.
3. Abra o terminal do PyCharm e execute:

```bash
python manage.py runserver
```

4. Acesse no navegador:

```
http://127.0.0.1:8000/
```

---

## Uso do Dashboard

**Filtros**:
  - **Região**: Filtra por região no município de São Paulo
  - **CEP**: Filtra por CEP específico
  - Ambos filtros podem ser combinados.

**Botões**:
  - **Aplicar Filtros**: Atualiza gráficos e tabela com os filtros selecionados.
  - **Limpar Filtros**: Reseta filtros e mostra todos os dados.
  - **Exportar CSV**: Baixa os dados da tabela com os filtros aplicados.

**Gráficos**:
  1. **Distribuição de Leitos Hospitalares por Região**  
  2. **Distribuição de Leitos SUS (Especialidades) por Região**  
  3. **Tendência Mensal de Leitos Totais x Leitos SUS por Região**

**Tabela**:
  1. Relação de Hospitais por Região

  **Paginação da Tabela**:
  - Botões **Anterior / Próxima** para navegar entre páginas.
  - Seleção de quantidade de registros por página.

---

## Backend
1. Na maquina Ubuntu, insira esses comando no terminal

```bash
sudo apt update
sudo apt install git python3-pip -y
git clone https://github.com/SEU_USUARIO/sp-api.git
cd UNIVESP-PI-IV
```

2. Instalar dependências

```bash
pip install -r requirements.txt
```

3. Rodar a API na VPS

```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Agora ela vai estar acessível em:

```bash
http://SEU_IP_PUBLICO:8000
(exemplo: http://20.45.11.180:8000/docs)
```