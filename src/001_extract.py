import os
import pandas as pd
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

# 1. Configurações Globais
load_dotenv()
# Ajustes de exibição do Pandas (útil para debug , nao é obrigatório)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

def conectar_banco():
    """Estabelece conexão com o PostgreSQL com logs de erro claros."""
    try:
        conn = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            connect_timeout=5 # Evita que o código trave se o banco estiver offline (boa prática)
        )
        return conn
    except Exception as e:
        print(f"❌ ERRO NO BANCO: Verifique se o PostgreSQL está rodando e o .env está correto. Detalhes: {e}")
        return None

def extrair_dados_sql():
    """Extrai funcionários do banco com verificação de DataFrame vazio."""
    conn = conectar_banco()
    if not conn: return None
    
    try:
        query = "SELECT * FROM funcionarios"
        df = pd.read_sql_query(query, conn)
        if df.empty:
            print("⚠️ AVISO: A tabela 'funcionarios' está vazia.")
        else:
            print(f"✅ SQL: {len(df)} funcionários extraídos.")
        return df
    except Exception as e:
        print(f"❌ ERRO NA QUERY: {e}")
        return None
    finally:
        conn.close()

def carregar_ocupacao():
    """Lê o CSV de ocupação com tratamento para arquivo inexistente."""
    caminho = r"data\raw\ocupacao\janeiro.csv"
    try:
        if not os.path.exists(caminho):
            print(f"❌ ERRO: Arquivo não encontrado em: {caminho}")
            return None
        
        df = pd.read_csv(caminho)
        print(f"✅ CSV: {len(df)} dias de ocupação carregados.")
        return df
    except Exception as e:
        print(f"❌ ERRO AO LER CSV: {e}")
        return None

def gerar_base_escala_inteligente():
    """Une as fontes de dados e gera a matriz final."""
    print("\n--- Iniciando Processamento de Dados ---")
    
    df_funcionarios = extrair_dados_sql()
    df_ocupacao = carregar_ocupacao()



    if df_funcionarios is None or df_ocupacao is None:
        print("🛑 FALHA: Não foi possível gerar a base pois uma das fontes falhou.")
        return None

    try:
        # Cross Join (Produto Cartesiano)
        df_escala = df_funcionarios.assign(k=1).merge(df_ocupacao.assign(k=1), on='k').drop('k', axis=1)
        
        # Ajuste de data (Assume que a coluna no CSV se chama 'data') 
        if 'data' in df_escala.columns:
            df_escala['data'] = pd.to_datetime(df_escala['data'], dayfirst=True)
        
        print(f"🚀 SUCESSO: Matriz gerada com {len(df_escala)} combinações.")
        print("\n--- PREVIEW DA MATRIZ ---")
        print(df_escala.head(10))
        return df_escala
    except Exception as e:
        print(f"❌ ERRO NO PROCESSAMENTO DA MATRIZ: {e}")
        return None

if __name__ == "__main__":
    base_final = gerar_base_escala_inteligente()
    
    def salvar_base_processada(df):
     if df is not None:
            caminho = r"data\processed\matriz_escala.csv"
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            df.to_csv(caminho, index=False, encoding='utf-8')
            print(f"💾 Base persistida para transformação: {caminho}")

if __name__ == "__main__":
    base_final = gerar_base_escala_inteligente()
    salvar_base_processada(base_final) 