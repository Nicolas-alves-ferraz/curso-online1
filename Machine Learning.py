# Importando as bibliotecas necessárias
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error


# Função para gerar os dados fictícios
def gerar_dados():
    # Dados fictícios sobre cursos online
    data = {
        'País': ['Brasil', 'EUA', 'Alemanha', 'França', 'Reino Unido', 'Brasil', 'EUA', 'Alemanha'],
        'Idioma': ['Português', 'Inglês', 'Alemão', 'Francês', 'Inglês', 'Português', 'Inglês', 'Alemão'],
        'Tema': ['Tecnologia', 'Negócios', 'Saúde', 'Tecnologia', 'Saúde', 'Negócios', 'Tecnologia', 'Saúde'],
        'Duração (horas)': [30, 40, 35, 45, 30, 50, 60, 25],
        'Nível de Dificuldade': ['Fácil', 'Médio', 'Difícil', 'Médio', 'Fácil', 'Médio', 'Difícil', 'Fácil'],
        'Preço (USD)': [100, 150, 120, 130, 110, 140, 160, 120],
        'Nº de Alunos': [200, 500, 400, 600, 300, 700, 800, 500]
    }
    return pd.DataFrame(data)


# Carregar os dados fictícios
df = gerar_dados()


# Pré-processamento dos dados
def pre_processamento(df):
    # Codificar variáveis categóricas
    encoder = OneHotEncoder(sparse=False)
    encoded_features = encoder.fit_transform(df[['País', 'Idioma', 'Tema', 'Nível de Dificuldade']])

    # Criar DataFrame com as variáveis codificadas
    encoded_df = pd.DataFrame(encoded_features,
                              columns=encoder.get_feature_names_out(['País', 'Idioma', 'Tema', 'Nível de Dificuldade']))

    # Concatenar com as variáveis numéricas
    df_processado = pd.concat([encoded_df, df[['Duração (horas)']]], axis=1)

    return df_processado


# Função para treinar e prever com o modelo escolhido
def treinar_e_prever(modelo, X_train, X_test, y_train):
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    return y_pred


# Interface com o Streamlit
st.title('Previsão de Preço e Número de Alunos de Cursos Online')

# Menu de escolha de predição
opcao = st.selectbox("Escolha o tipo de previsão", ("Preço do Curso", "Número de Alunos"))

# Pre-processamento dos dados
df_processado = pre_processamento(df)

if opcao == "Preço do Curso":
    # Variáveis de entrada para preço do curso
    X = df_processado[['País_Brasil', 'País_EUA', 'País_Alemanha', 'País_França', 'País_Reino Unido',
                       'Idioma_English', 'Idioma_Portuguese', 'Idioma_German', 'Idioma_French',
                       'Tema_Tecnologia', 'Tema_Negócios', 'Tema_Saúde', 'Tema_Arte', 'Tema_Ciência',
                       'Nível de Dificuldade_Fácil', 'Nível de Dificuldade_Médio', 'Nível de Dificuldade_Difícil',
                       'Duração (horas)']]
    y = df['Preço (USD)']

    # Divisão em treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Escolher o modelo
    modelo = st.selectbox("Escolha o modelo", ("Árvore de Decisão", "KNN"))

    if modelo == "Árvore de Decisão":
        # Árvore de decisão
        profundidade = st.slider("Profundidade da Árvore", min_value=1, max_value=10, value=3)
        modelo_escolhido = DecisionTreeRegressor(max_depth=profundidade)
    elif modelo == "KNN":
        # KNN
        k_vizinhos = st.slider("Número de Vizinhos (K)", min_value=1, max_value=10, value=5)
        modelo_escolhido = KNeighborsRegressor(n_neighbors=k_vizinhos)

    # Treinamento e previsão
    y_pred = treinar_e_prever(modelo_escolhido, X_train, X_test, y_train)

    # Exibir resultado
    erro = mean_absolute_error(y_test, y_pred)
    st.write(f"Erro Absoluto Médio: {erro:.2f} USD")
    st.write(f"Preço Previsto: {y_pred[0]:.2f} USD")

elif opcao == "Número de Alunos":
    # Variáveis de entrada para o número de alunos
    X = df_processado[['País_Brasil', 'País_EUA', 'País_Alemanha', 'País_França', 'País_Reino Unido',
                       'Idioma_English', 'Idioma_Portuguese', 'Idioma_German', 'Idioma_French',
                       'Tema_Tecnologia', 'Tema_Negócios', 'Tema_Saúde', 'Tema_Arte', 'Tema_Ciência',
                       'Nível de Dificuldade_Fácil', 'Nível de Dificuldade_Médio', 'Nível de Dificuldade_Difícil',
                       'Duração (horas)']]
    y = df['Nº de Alunos']

    # Divisão em treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Escolher o modelo
    modelo = st.selectbox("Escolha o modelo", ("Árvore de Decisão", "KNN"))

    if modelo == "Árvore de Decisão":
        profundidade = st.slider("Profundidade da Árvore", min_value=1, max_value=10, value=3)
        modelo_escolhido = DecisionTreeRegressor(max_depth=profundidade)
    elif modelo == "KNN":
        k_vizinhos = st.slider("Número de Vizinhos (K)", min_value=1, max_value=10, value=5)
        modelo_escolhido = KNeighborsRegressor(n_neighbors=k_vizinhos)

    # Treinamento e previsão
    y_pred = treinar_e_prever(modelo_escolhido, X_train, X_test, y_train)

    # Exibir resultado
