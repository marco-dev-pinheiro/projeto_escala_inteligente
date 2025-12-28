import streamlit as st
import pandas as pd
import plotly.express as px
import os  
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io


# Configuração da página
st.set_page_config(page_title="Escala Inteligente - Hotel", layout="wide")

def carregar_dados():
    caminho = "outputs/relatorios_excel/escala_inteligente_final.csv"
    if os.path.exists(caminho):
        df = pd.read_csv(caminho)
        df['data'] = pd.to_datetime(df['data'])
        return df
    return None
#------------- Função para gerar PDF da escala -------------#



def gerar_pdf(df_escala):
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=landscape(letter))
    elements = []
    
    # Cabeçalho
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Escala Inteligente de Trabalho - Hotel", styles['Title']))
    
    # Preparar dados para a tabela do PDF
    data = [["Colaborador"] + list(df_escala.columns)] # Cabeçalho da tabela
    for index, row in df_escala.iterrows():
        data.append([index] + list(row.values))
    
    # Estilização da Tabela
    t = Table(data)
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ])
    
    # Cores dinâmicas para as células
    for row_idx, row_data in enumerate(data[1:], start=1):
        for col_idx, value in enumerate(row_data[1:], start=1):
            if value == 'TRABALHO':
                estilo.add('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.lightpink)
            elif value == 'FOLGA_POSSIVEL':
                estilo.add('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.lightgreen)
                
    t.setStyle(estilo)
    elements.append(t)
    
    doc.build(elements)
    return output.getvalue()



def main():
    st.title("🏨 Dashboard de Gestão de Escala Inteligente")
    st.markdown("---")

    df = carregar_dados()

    if df is None:
        st.error("❌ Arquivo de dados não encontrado! Rode o script '002_transform.py' primeiro.")
        return

    # --- SIDEBAR (Filtros) ---
    st.sidebar.header("Filtros")
    funcionarios = st.sidebar.multiselect("Selecionar Funcionários", df['nome'].unique(), default=df['nome'].unique()[:3])
    
                                                    # --- MÉTRICAS PRINCIPAIS ---
    col1, col2, col3 = st.columns(3)
    media_ocupacao = df['ocupacao'].mean()
    col1.metric("Ocupação Média", f"{media_ocupacao:.2f}%")
    col2.metric("Total de Registros", len(df))
    col3.metric("Status Operacional", "Otimizado por IA" if 'insight_ia' in df.columns else "Lógica Local")
                                                # --- GRÁFICO DE OCUPAÇÃO ---
    st.subheader("📈 Tendência de Ocupação e Status de Trabalho")
    df_filtered = df[df['nome'].isin(funcionarios)]
        
        # Filtro opcional: mostrar apenas dias de trabalho
    mostrar_apenas_trabalho = st.sidebar.checkbox("Mostrar apenas dias de trabalho", value=False)
    if mostrar_apenas_trabalho:
        df_filtered = df_filtered[df_filtered['status_escala'] == 'TRABALHO']

    
    fig_ocupacao = px.line(df.drop_duplicates('data'), x='data', y='ocupacao', 
                          title="Ocupação do Hotel ao Longo do Tempo",
                          line_shape="spline", render_mode="svg")
    st.plotly_chart(fig_ocupacao, use_container_width=True)

   # --- VISUALIZAÇÃO DA ESCALA ---
 
    df_filtered['data_formatada'] = (
        df_filtered['data'].dt.strftime('%d/%m/%Y') + " \n " + df_filtered['semana']
    )

                                             # --- VISUALIZAÇÃO DA ESCALA ---
    st.subheader("🗓️ Tabela de Escala Sugerida")
    
    #  'data_formatada' como colunas na pivot table
    df_filtered['data_formatada'] = ( df_filtered['data'].dt.strftime('%d/%m/%Y') + " \n " + df_filtered['semana'] )
    escala_view = df_filtered.pivot_table(
        index='nome', 
        columns='data_formatada',  # <--- Coluna nova aqui
        values='status_escala', 
        aggfunc='first'
    ).fillna("-")

    # Ordenar as colunas para garantir que fiquem na sequência cronológica
    # (O pivot_table pode bagunçar a ordem ao transformar em string)
    ordem_colunas = df_filtered.sort_values('data')['data_formatada'].unique()
    escala_view = escala_view.reindex(columns=ordem_colunas)
    
                             # Exibição com o estilo corrigido (usando .map em vez de .applymap para evitar avisos)
    st.subheader("🗓️ Tabela de Escala Sugerida")

    escala_view = df_filtered.pivot_table(
        index='nome',
        columns='data_formatada',
        values='status_escala',
        aggfunc='first'
    ).fillna("-")

    # Botão de download do PDF
    pdf_data = gerar_pdf(escala_view)
    st.download_button(
        label="📥 Baixar Escala em PDF para Impressão",
        data=pdf_data,
        file_name="escala_hotel_6x1.pdf",
        mime="application/pdf",
    )

    ordem_colunas = df_filtered.sort_values('data')['data_formatada'].unique()
    escala_view = escala_view.reindex(columns=ordem_colunas)

    st.dataframe(
        escala_view.style.map(
            lambda x: 'background-color: #d4edda; color: #155724' if x == 'TRABALHO'
            else 'background-color: #f8d7da; color: #721c24' if x == 'FOLGA_POSSIVEL'
            else ''
        ),
        use_container_width=True
    )

    # Legenda objetiva
    st.caption("Legenda: verde = trabalho confirmado; vermelho = folga sugerida; '-' = sem dado.")

                                                # --- INSIGHTS DA IA ---
                                        # --- INSIGHTS DA IA E RECOMENDAÇÃO ---
    st.markdown("---")
    st.subheader("🤖 Análise Estratégica da IA")
        
        # Identifica dias de ocupação abaixo de 30%
    dias_baixa = df[df['ocupacao'] < 30][['data', 'ocupacao']].drop_duplicates()
        
    col_ia, col_equipe = st.columns(2)
        
    
    with col_ia:
        st.info("💡 **Dias de Baixa Ocupação (Sugerido para Folgas):**")
        if not dias_baixa.empty:
            for _, row in dias_baixa.head(5).iterrows():
                st.write(f"- {row['data'].strftime('%d/%m/%Y')}: {row['ocupacao']:.1f}% de ocupação.")
        else:
            st.write("Ocupação estável no período.")

    
    with col_equipe:
        with col_equipe:
            st.success("👥 **Sugestão de Equipe por Turno:**")
            st.write("**Manhã:** Santana (Sup) + 3 Recep + 1 Manobrista")
            st.write("**Tarde:** 3 Recep + 1 Manobrista")
            st.caption("Nota: Nos dias verdes (Trabalho), manter 100% da escala.")


                                           # --- DISTRIBUIÇÃO POR TURNO ---
    st.subheader("📊 Distribuição de Colaboradores por Turno")
    
                                       # Agrupa por turno contando nomes únicos
    df_turnos = df.groupby('turno')['nome'].nunique().reset_index()
    df_turnos.columns = ['turno', 'quantidade']
    
    fig_turno = px.pie(df_turnos, values='quantidade', names='turno', 
                       title="Equipe por Turno (Total de Funcionários)")
    st.plotly_chart(fig_turno, use_container_width=True)
if __name__ == "__main__":
    main()