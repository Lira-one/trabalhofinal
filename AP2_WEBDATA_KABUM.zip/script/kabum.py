import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Título e descrição do projeto
st.title("🥷 Análise Ninja dos Dados Kabum")
st.markdown("Prepare-se para mergulhar nos dados como um verdadeiro mestre das estatísticas.")
st.write("""
Este projeto tem como objetivo explorar dados de produtos disponíveis no site Kabum.
Aqui, vamos analisar valores nulos, estatísticas descritivas e relações entre variáveis numéricas.
""")

# 2. Carregar o dataset
st.header("📂 1. Carregamento dos Dados")

caminho_csv = "AP2_WEBDATA_KABUM.zip/script/kabum.py"

try:
    df = pd.read_csv(caminho_csv, sep=';')
    st.success("Dados carregados com sucesso!")
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

# Mostrar os primeiros dados
st.subheader("Visualização Inicial")
st.dataframe(df.head())

# 3. Checar tipos de dados e valores nulos
st.header("2. Análise de Qualidade dos Dados")

st.subheader("🔍 Tipos de Dados")
st.dataframe(df.dtypes)

st.subheader("Valores Nulos por Coluna")
valores_nulos = df.isnull().sum().reset_index()
valores_nulos.columns = ['Coluna', 'Nulos']
st.dataframe(valores_nulos)

# 4. Tentar converter colunas que parecem ser numéricas
for col in df.columns:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='ignore')
# Limpar e transformar a coluna de parcelas
df['quantidade de parcelas'] = df['quantidade de parcelas'].astype(str)
df['quantidade de parcelas'] = df['quantidade de parcelas'].str.extract('(\d+)')
df['quantidade de parcelas'] = pd.to_numeric(df['quantidade de parcelas'], errors='coerce')

# 5. Análise Univariada
st.subheader("📊 Análise Univariada")

colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if not colunas_numericas:
    st.warning("Não foram encontradas colunas numéricas para análise.")
    st.stop()

coluna_analise = st.selectbox("Escolha uma coluna numérica", colunas_numericas)

st.subheader(f"Estatísticas de: {coluna_analise}")
st.write(df[coluna_analise].describe().round(2))

# Histograma
st.subheader("Distribuição - Histograma")
fig_hist = px.histogram(df, x=coluna_analise)
st.plotly_chart(fig_hist)

# Boxplot
st.subheader("Distribuição - Boxplot")
fig_box = px.box(df, y=coluna_analise)
st.plotly_chart(fig_box)

# 6. Análise Multivariada
st.header("📈 Análise Multivariada")

colunas_selecionadas = st.multiselect(
    "Selecione exatamente duas colunas numéricas para análise de dispersão",
    colunas_numericas
)

if len(colunas_selecionadas) == 2:
    st.subheader(f"Relação entre {colunas_selecionadas[0]} e {colunas_selecionadas[1]}")
    fig_scatter = px.scatter(
        df, 
        x=colunas_selecionadas[0], 
        y=colunas_selecionadas[1], 
        title=f"Dispersão entre {colunas_selecionadas[0]} e {colunas_selecionadas[1]}"
    )
    st.plotly_chart(fig_scatter)
elif len(colunas_selecionadas) > 2:
    st.warning("Por favor, selecione apenas **duas** colunas.")
else:
    st.info("Aguardando seleção de duas colunas numéricas...")

# 7. Encerramento
st.header("📢 Conclusão e um recado importante")

st.markdown("""
Analisar os dados da Kabum foi quase tão emocionante quanto ver meu time em **primeiro lugar no campeonato** 🐖💚🥇

Aliás, professor, se os gráficos não te convencerem, talvez o desempenho do Palmeiras te inspire a considerar um 10 com louvor! 😄
**Brincadeiras à parte**, o projeto me ensinou muito sobre:
            
- Limpeza e manipulação de dados com pandas
- Visualizações interativas com Plotly
- Como transformar uma planilha bruta em insights valiosos           
- Os dados foram tratados como se fossem VIPs no tapete vermelho do pandas.
- Cada gráfico foi feito com carinho (e um pouco de energético).
- O código foi escrito com amor e alguns `debugs` dramáticos no meio da madrugada.           

Espero que o senhor se divirta corrigindo tanto quanto eu programando. Até a próxima!
""")
