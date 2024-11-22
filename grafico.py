# Importando as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ---------------------------------
# 1. Popularidade por Tema de Cursos em Cada País
# ---------------------------------

# Dados fictícios de popularidade por tema e país
data_popularidade = {
    'País': ['Brasil', 'EUA', 'Alemanha', 'França', 'Reino Unido'],
    'Tecnologia': [50, 70, 60, 40, 65],
    'Saúde': [30, 20, 40, 50, 30],
    'Negócios': [20, 10, 10, 10, 5],
}

df_popularidade = pd.DataFrame(data_popularidade)

# Gráfico de barras empilhadas para popularidade de cursos por tema em cada país
fig = px.bar(df_popularidade, x='País', y=['Tecnologia', 'Saúde', 'Negócios'],
             title="Popularidade de Cursos por Tema e País",
             labels={"value": "Popularidade", "variable": "Tema"})
fig.show()

# ---------------------------------
# 2. Preços Médios por Idioma e País
# ---------------------------------

# Dados fictícios de preços médios por idioma e país
data_precos = {
    'País': ['Brasil', 'EUA', 'Alemanha', 'França', 'Reino Unido'],
    'Inglês': [100, 150, 120, 130, 140],
    'Português': [80, 100, 95, 90, 110],
    'Alemão': [120, 130, 115, 140, 135],
}

df_precos = pd.DataFrame(data_precos)

# Gráfico de barras para comparar os preços médios por idioma e país
df_precos.set_index('País').T.plot(kind='bar', stacked=False)
plt.title('Preços Médios por Idioma e País')
plt.ylabel('Preço Médio (USD)')
plt.show()

# ---------------------------------
# 3. Distribuição de Alunos por Área de Estudo ou Tipo de Curso
# ---------------------------------

# Dados fictícios de distribuição de alunos por área de estudo
labels = ['Tecnologia', 'Negócios', 'Saúde', 'Arte', 'Ciência']
sizes = [40, 25, 15, 10, 10]

# Gráfico de pizza para distribuição de alunos por área de estudo
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Distribuição de Alunos por Área de Estudo")
plt.show()

# ---------------------------------
# 4. Mapa Interativo de Popularidade de Cursos por País
# ---------------------------------

# Dados fictícios para visualização em mapa
data_mapa = {
    'País': ['Brasil', 'EUA', 'Alemanha', 'França', 'Reino Unido'],
    'Popularidade': [60, 85, 70, 50, 65],
    'Latitude': [-14.2350, 37.0902, 51.1657, 46.6034, 51.5074],
    'Longitude': [-51.9253, -95.7129, 10.4515, 1.8883, -0.1278],
}

df_mapa = pd.DataFrame(data_mapa)

# Criando um mapa interativo para mostrar a popularidade dos cursos por país
fig_mapa = px.scatter_geo(df_mapa, lat='Latitude', lon='Longitude', color='Popularidade',
                          size='Popularidade', hover_name='País', projection="natural earth",
                          title="Popularidade de Cursos por País")
fig_mapa.show()
