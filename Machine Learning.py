from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error

app = Flask(__name__)


# Função para gerar os dados fictícios
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


# Função para pré-processamento
def pre_processamento(df):
    encoder = OneHotEncoder(sparse_output=False)
    encoded_features = encoder.fit_transform(df[['País', 'Idioma', 'Tema', 'Nível de Dificuldade']])
    encoded_df = pd.DataFrame(encoded_features,
                              columns=encoder.get_feature_names_out(['País', 'Idioma', 'Tema', 'Nível de Dificuldade']))
    df_processado = pd.concat([encoded_df, df[['Duração (horas)']]], axis=1)
    return df_processado


# Função para treinar e prever
def treinar_e_prever(modelo, X_train, X_test, y_train):
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    return y_pred


@app.route('/')
def index():
    return render_template('Grafico.html')


@app.route('/prever', methods=['POST'])
def prever():
    global modelo
    dados = request.json
    opcao = dados['opcao']
    modelo_escolhido = dados['modelo']
    parametros = dados['parametros']

    df = gerar_dados()
    df_processado = pre_processamento(df)

    if opcao == 'Preço do Curso':
        X = df_processado[['País_Brasil', 'País_EUA', 'País_Alemanha', 'País_França', 'País_Reino Unido',
                           'Idioma_English', 'Idioma_Portuguese', 'Idioma_German', 'Idioma_French',
                           'Tema_Tecnologia', 'Tema_Negócios', 'Tema_Saúde', 'Nível de Dificuldade_Fácil',
                           'Nível de Dificuldade_Médio', 'Nível de Dificuldade_Difícil', 'Duração (horas)']]
        y = df['Preço (USD)']
    elif opcao == 'Número de Alunos':
        X = df_processado[['País_Brasil', 'País_EUA', 'País_Alemanha', 'País_França', 'País_Reino Unido',
                           'Idioma_English', 'Idioma_Portuguese', 'Idioma_German', 'Idioma_French',
                           'Tema_Tecnologia', 'Tema_Negócios', 'Tema_Saúde', 'Nível de Dificuldade_Fácil',
                           'Nível de Dificuldade_Médio', 'Nível de Dificuldade_Difícil', 'Duração (horas)']]
        y = df['Nº de Alunos']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    if modelo_escolhido == 'Árvore de Decisão':
        profundidade = parametros['profundidade']
        modelo = DecisionTreeRegressor(max_depth=profundidade)
    elif modelo_escolhido == 'KNN':
        k_vizinhos = parametros['k_vizinhos']
        modelo = KNeighborsRegressor(n_neighbors=k_vizinhos)

    y_pred = treinar_e_prever(modelo, X_train, X_test, y_train)
    erro = mean_absolute_error(y_test, y_pred)

    return jsonify({'erro': erro, 'previsoes': y_pred.tolist()})


if __name__ == '__main__':
    app.run(debug=True)
