import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from openai import OpenAI 
from dotenv import load_dotenv # Versão moderna da biblioteca (v1.0+)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o cliente OpenAI (Certifique-se de ter a variável de ambiente OPENAI_API_KEY)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def limpar_e_preparar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza nomes de colunas e converte valores numéricos brasileiros para float.
    """
    # 1. Remove espaços e padroniza para minúsculo
    df.columns = df.columns.str.strip().str.lower()
    
    # 2. Renomeia 'ocupacao_porcentagem' para 'ocupacao' para facilitar o código
    if 'ocupacao_porcentagem' in df.columns:
        df = df.rename(columns={'ocupacao_porcentagem': 'ocupacao'})
    
    # 3. Tratamento de números: transforma "16,35" em 16.35
    if df['ocupacao'].dtype == 'object':
        df['ocupacao'] = df['ocupacao'].str.replace(',', '.').astype(float)
    
    return df

def aplicar_transformacao_local(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformação com lógica 6x1: 6 dias de trabalho e 1 de folga.
    Prioriza folgas em dias de menor ocupação.
    """
    df = df.sort_values(['nome', 'data'])
    df['status_escala'] = 'TRABALHO'
    
    for nome in df['nome'].unique():
        indices = df[df['nome'] == nome].index
        # A cada bloco de 7 dias, define o dia de menor ocupação como folga
        for i in range(0, len(indices), 7):
            bloco = indices[i:i+7]
            if len(bloco) > 0:
                id_folga = df.loc[bloco, 'ocupacao'].idxmin()
                df.at[id_folga, 'status_escala'] = 'FOLGA_POSSIVEL'
    
    # Reforço: qualquer célula não marcada como folga é TRABALHO
    df['status_escala'] = df['status_escala'].fillna('TRABALHO')
    # Coluna auxiliar para filtros no dashboard
    df['dia_trabalho'] = (df['status_escala'] == 'TRABALHO')
   
    return df


def aplicar_transformacao_openai(df: pd.DataFrame) -> pd.DataFrame:
    """
    Envia uma amostra dos dados (uma semana) para a IA gerar a estratégia.
    Nota: Enviar 372 (um mes) registros pode exceder o limite de tokens; focamos no resumo.
    """
    # Pegamos apenas os primeiros 7 dias para a IA analisar a lógica
    amostra_dados = df[['data', 'semana', 'ocupacao']].head(7).to_dict(orient='records')

    prompt = f"""
    Atue como um Especialista em Escalas Hoteleiras (6x1).
    Analise estes dados de ocupação e sugira a distribuição de folgas para a equipe:
    
    DADOS DE OCUPAÇÃO (Próximos 7 dias):
    {amostra_dados}

    REGRAS:
    1. Equipe: Santana (Sup), Marcelo, Bruno, Gui, Mariana, Denilson, Marco, Noé, Jefferson, João.
    2. Cobertura: Manhã e Tarde (Mínimo 3 Recep + 1 Manobrista).
    3. Restrição: Máximo 6 dias seguidos de trabalho.
    4. Alternar para um de cada eqipe folgar por dia (se possível).
    5. Folgas alternadas 
    
    SAÍDA DESEJADA:
    Retorne uma tabela Markdown com a sugestão de folgas e uma breve explicação da lógica para os manobristas.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um gestor de RH hoteleiro focado em otimização de custos e satisfação da equipe."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        sugestao_ia = response.choices[0].message.content
        print("\n🤖 SUGESTÃO DA IA PARA A SEMANA:\n")
        print(sugestao_ia)
        
        # Adicionamos a sugestão como um metadado no DataFrame (opcional)
        df['insight_ia'] = "Veja o log do console para a tabela completa"
        
    except Exception as e:
        print(f"⚠️ Erro na API OpenAI: {e}")
    
    return df

def pipeline_etl(use_openai: bool = False):
    """
    Pipeline principal: Extração -> Limpeza -> Transformação -> Carga.
    """
    caminho_entrada = "data/processed/matriz_escala.csv"
    caminho_saida = "outputs/relatorios_excel/escala_inteligente_final.csv"

    if not os.path.exists(caminho_entrada):
        print(f"❌ Arquivo não encontrado: {caminho_entrada}")
        return

    print("🚀 Iniciando Pipeline de Transformação...")
    
    # 1. Extração
    df = pd.read_csv(caminho_entrada)
    
    # 2. Limpeza e Normalização (CORRIGE O KEYERROR)
    df = limpar_e_preparar_dados(df)
    
    # 3. Transformação
    if use_openai:
        df = aplicar_transformacao_openai(df)
        # Também rodamos a local para ter os números
        df = aplicar_transformacao_local(df)
    else:
        df = aplicar_transformacao_local(df)

    # 4. Carga (Salvamento)
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    df.to_csv(caminho_saida, index=False)
    
    print(f"✅ Sucesso! {len(df)} registros processados e salvos em: {caminho_saida}")

if __name__ == "__main__":
    # Para usar OpenAI, certifique-se de que OPENAI_API_KEY está no seu sistema
    pipeline_etl(use_openai=True)