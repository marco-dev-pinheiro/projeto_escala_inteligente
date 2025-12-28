para rodar a dashboard - streamlit run src/003_load_dashboard.py


mindmap
  root((Escala Inteligente))
    Engenharia de Dados
      Extração
        SQL / CSV Bruto
        Pandas Dataframes
      Transformação
        Limpeza de Dados
        Normalização de Ocupação
        Lógica Trabalhista 6x1
    Inteligência Artificial
      OpenAI GPT-4
        Análise de Tendências
        Estratégia de Equipe
        Prompt Engineering
    Interface e Entrega
      Dashboard Streamlit
        Filtros Interativos
        Gráficos de Turno e Ocupação
        Heatmap de Escala
      Exportação
        Relatórios em PDF
        Impressão Técnica
    Segurança e Portfólio
      Boas Práticas
        Ambiente Virtual - venv
        Variáveis de Ambiente - .env
        Documentação - README.md

        
# 🏨 Escala Inteligente: Otimização Hoteleira com IA

Este projeto é uma solução completa de **Data Engineering** e **Business Intelligence** para gestão de escalas hoteleiras. O sistema automatiza a criação de escalas no regime 6x1, cruzando dados de ocupação histórica com inteligência artificial para otimizar a força de trabalho.

## 🚀 Funcionalidades Principais

* **Pipeline ETL Automatizado:** Extração de dados (SQL), limpeza e normalização de métricas de ocupação.
* **Algoritmo de Escala 6x1:** Lógica customizada que garante 1 folga a cada 6 dias trabalhados, priorizando folgas em dias de baixa demanda.
* **Integração com OpenAI (GPT-4):** Análise qualitativa dos dados para geração de insights estratégicos para a gerência.
* **Dashboard Interativo:** Visualização em tempo real de métricas, gráficos de ocupação e distribuição de turnos via Streamlit.
* **Exportação PDF:** Geração de escala formatada e colorida pronta para impressão.

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Pandas & Scikit-learn:** Processamento de dados e normalização.
* **OpenAI API:** Inteligência artificial para análise de estratégia.
* **Streamlit & Plotly:** Dashboard web e gráficos interativos.
* **ReportLab:** Geração dinâmica de documentos PDF.

## 📂 Estrutura do Projeto

```text
projeto_escala_inteligente/
├── data/               # Dados brutos e processados
├── src/                # Scripts do sistema
│   ├── 001_extract.py  # Conexão e extração
│   ├── 002_transform.py# Lógica 6x1 e IA
│   └── 003_dashboard.py# Interface visual e PDF
├── outputs/            # Relatórios gerados (CSV/PDF)
├── .env                # Chaves de API (não versionar)
└── requirements.txt    # Dependências do projeto
```

# Como rodar ?
*** abaixo as instruçoes detalhadas para 
1- instalar  configurar e rodar  " leia atentamente "

2- Divirta-se clone melhore e de dicas de como posso melhorar . 

3- Para saber sobre proximos passos siga no linkedin , de feedback , deixe sugestoes.

Projeto Escala Inteligente - Gestão Hoteleira
Este sistema automatiza a criação de escalas de trabalho para hotéis seguindo o regime 6x1, utilizando Inteligência Artificial (OpenAI) para otimizar as folgas com base na ocupação do hotel.

# 📋 Pré-requisitos
Antes de começar, você precisará ter instalado:

Python 3.10 ou superior

Git (opcional, para versionamento)

#  ⚙️ Instalação e Configuração
1. Clonar o projeto

PowerShell

git clone https://github.com/seu-usuario/projeto_escala_inteligente.git
cd projeto_escala_inteligente

2. Criar Ambiente Virtual (Virtual Env)
É altamente recomendado usar um ambiente isolado:
----------------------------------------
PowerShell

python -m venv env
.\env\Scripts\activate
3. Instalar Dependências
Instale todas as bibliotecas necessárias de uma vez:

PowerShell

pip install -r requirements.txt
4. Configurar Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do projeto e adicione sua chave da API:
----------------------------------------------------------------------------
Plaintext

OPENAI_API_KEY=sk-sua_chave_aqui


#### Como executar #####

🚀 Como Executar o Projeto
O projeto segue um fluxo lógico de três etapas. Você deve rodar os scripts nesta ordem:

Passo 1: Extração de Dados
Extrai as informações brutas do banco de dados/CSV inicial.

PowerShell

python src/001_extract.py
Passo 2: Inteligência e Transformação (Lógica 6x1)
Processa a escala, aplica a regra de 6 dias de trabalho por 1 de folga e gera os insights da IA.

PowerShell

python src/002_transform.py
Passo 3: Dashboard Interativo
Abre a interface visual e permite a exportação da escala em PDF.

PowerShell
--------------------------------------------------------------------------
## comando para rodar a dashboar ##
streamlit run src/003_load_dashboard.py

-----------------------------------------------------------------------------


