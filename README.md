1. Importação das Bibliotecas
Primeiro, importamos as bibliotecas necessárias:

import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error

pandas: Para manipulação e análise de dados em formato de tabelas (DataFrames).
numpy: Para operações numéricas (não é muito usado diretamente aqui, mas é necessário para cálculos do modelo).
streamlit: Para criar a interface interativa onde o usuário pode selecionar opções e ver os resultados.
sklearn: Biblioteca de aprendizado de máquina. Usamos várias funcionalidades:
train_test_split: Para dividir os dados em conjuntos de treino e teste.
OneHotEncoder: Para converter variáveis categóricas (como "País" ou "Idioma") em números, o que é necessário para os modelos de machine learning.
DecisionTreeRegressor e KNeighborsRegressor: Modelos de aprendizado supervisionado para prever valores contínuos (como o preço ou número de alunos).
mean_absolute_error: Para calcular a diferença entre as previsões feitas pelo modelo e os valores reais.

2. Função para Gerar Dados Fictícios
A função gerar_dados() cria um DataFrame com dados fictícios de cursos online, com várias características como país, idioma, tema, duração, nível de dificuldade, preço e número de alunos.

def gerar_dados():
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
Esta função cria um conjunto de dados de cursos online com várias características (como preço, duração, nível de dificuldade, etc.), o que é útil para prever o preço ou o número de alunos que um curso pode atrair.


3. Função para Pré-processamento dos Dados
A função pre_processamento() converte as variáveis categóricas em formato numérico para que o modelo de aprendizado de máquina possa entender e usá-las.

def pre_processamento(df):
    # Codificar variáveis categóricas
    encoder = OneHotEncoder(sparse=False)
    encoded_features = encoder.fit_transform(df[['País', 'Idioma', 'Tema', 'Nível de Dificuldade']])
    
    # Criar DataFrame com as variáveis codificadas
    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['País', 'Idioma', 'Tema', 'Nível de Dificuldade']))
    
    # Concatenar com as variáveis numéricas
    df_processado = pd.concat([encoded_df, df[['Duração (horas)']]], axis=1)
    
    return df_processado
Aqui, a função OneHotEncoder é usada para transformar dados categóricos, como o país ou idioma, em variáveis numéricas. Por exemplo, "Brasil" se torna uma coluna com valores 0 ou 1 (onde 1 significa que o curso é do Brasil). Isso permite que o modelo de aprendizado de máquina use essas variáveis nas previsões.

4. Função para Treinar e Fazer Previsões
A função treinar_e_prever() treina o modelo com os dados de entrada e faz previsões com base nos dados de teste.

def treinar_e_prever(modelo, X_train, X_test, y_train):
    modelo.fit(X_train, y_train)  # Treina o modelo com os dados
    y_pred = modelo.predict(X_test)  # Faz previsões usando o modelo treinado
    return y_pred
Aqui, o modelo escolhido (seja Árvore de Decisão ou KNN) é treinado usando os dados de treino e depois faz previsões com os dados de teste.

5. Interface com o Streamlit
O código abaixo cria a interface gráfica que o usuário pode interagir com.

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
        profundidade = st.slider("Profundidade da Árvore", min_value=1, max_value=10, value=3)
        modelo_escolhido = DecisionTreeRegressor(max_depth=profundidade)
    elif modelo == "KNN":
        k_vizinhos = st.slider("Número de Vizinhos (K)", min_value=1, max_value=10, value=5)
        modelo_escolhido = KNeighborsRegressor(n_neighbors=k_vizinhos)
    
    # Treinamento e previsão
    y_pred = treinar_e_prever(modelo_escolhido, X_train, X_test, y_train)
    
    # Exibir resultado
    erro = mean_absolute_error(y_test, y_pred)
    st.write(f"Erro Absoluto Médio: {erro:.2f} USD")
    st.write(f"Preço Previsto: {y_pred[0]:.2f} USD")
    
Título: Define o título da página.
Menu de Escolha: O usuário escolhe se quer prever o preço do curso ou o número de alunos.
Pré-processamento: O código pré-processa os dados para que eles possam ser usados no modelo.
Escolha do Modelo: O usuário pode escolher entre a Árvore de Decisão ou KNN.
Treinamento e Previsão: O modelo é treinado com os dados e faz uma previsão com base nos dados de teste.
Exibição do Resultado: O erro da previsão (em valor absoluto) e a previsão feita são exibidos para o usuário.

6. Interação com o Usuário
O Streamlit permite que o usuário interaja com a interface e veja como diferentes ajustes (como profundidade da árvore ou número de vizinhos) afetam a previsão.
O resultado final é a previsão do preço ou o número de alunos com base nas escolhas feitas pelo usuário.
