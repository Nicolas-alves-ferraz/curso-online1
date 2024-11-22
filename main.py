import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Função para gerar gráficos automaticamente
def gerar_graficos(df):
    # Gráfico de Distribuição de Preços
    st.subheader('Distribuição de Preços dos Cursos')
    fig, ax = plt.subplots()
    sns.histplot(df['preco'], kde=True, ax=ax, color='blue')
    ax.set_title('Distribuição dos Preços')
    st.pyplot(fig)

    # Gráfico de Distribuição das Avaliações
    st.subheader('Distribuição das Avaliações (Ratings)')
    fig, ax = plt.subplots()
    sns.histplot(df['rating'], kde=True, ax=ax, color='green')
    ax.set_title('Distribuição das Avaliações')
    st.pyplot(fig)

    # Boxplot para Duração dos Cursos
    st.subheader('Boxplot da Duração dos Cursos')
    fig, ax = plt.subplots()
    sns.boxplot(x=df['duracao'], ax=ax, color='purple')
    ax.set_title('Boxplot da Duração dos Cursos')
    st.pyplot(fig)

    # Mapa de Calor para Verificar Correlação
    st.subheader('Correlação entre Variáveis Numéricas')
    correlacao = df[['preco', 'rating', 'duracao', 'num_alunos']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(correlacao, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlação entre Variáveis')
    st.pyplot(fig)

# Função para carregar e validar o arquivo CSV
def carregar_csv(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            # Verificando se o arquivo possui as colunas necessárias
            colunas_necessarias = ['nome_curso', 'preco', 'rating', 'duracao', 'num_alunos', 'categoria']
            for coluna in colunas_necessarias:
                if coluna not in df.columns:
                    st.warning(f'A coluna "{coluna}" não foi encontrada no arquivo CSV.')
                    return None
            return df
        except Exception as e:
            st.error(f'Erro ao carregar o arquivo CSV: {e}')
            return None
    else:
        st.warning("Por favor, faça o upload de um arquivo CSV.")
        return None

# Função principal da interface Streamlit
def main():
    st.title('Analisador de Dados de Cursos Online')

    # Upload do arquivo CSV
    uploaded_file = st.file_uploader("Faça o upload de um arquivo CSV com dados de cursos online", type=["csv"])

    # Se o arquivo for enviado, carregar os dados e mostrar as análises
    if uploaded_file is not None:
        df = carregar_csv(uploaded_file)

        if df is not None:
            # Mostrar as primeiras linhas do DataFrame
            st.subheader('Visualização dos Dados')
            st.write(df.head())

            # Exibir estatísticas descritivas
            st.subheader('Estatísticas Descritivas')
            st.write(df.describe())

            # Gerar gráficos
            gerar_graficos(df)

if __name__ == '__main__':
    main()