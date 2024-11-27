from flask import Flask, render_template
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)

@app.route('/')
def index():
    # ---------------------------------
    # 1. Popularidade por Tema de Cursos em Cada País
    # ---------------------------------
    data_popularidade = {
        'País': ['Brasil', 'EUA', 'Alemanha', 'França', 'Reino Unido'],
        'Tecnologia': [50, 70, 60, 40, 65],
        'Saúde': [30, 20, 40, 50, 30],
        'Negócios': [20, 10, 10, 10, 5],
    }
    df_popularidade = pd.DataFrame(data_popularidade)

    fig_popularidade = px.bar(df_popularidade, x='País', y=['Tecnologia', 'Saúde', 'Negócios'],
                              title="Popularidade de Cursos por Tema e País",
                              labels={"value": "Popularidade", "variable": "Tema"})

    # ---------------------------------
    # 2. Preços Médios por Idioma e País
    # ---------------------------------
    data_precos = {
        'País': ['Brasil', 'EUA', 'Alemanha', 'França', 'Reino Unido'],
        'Inglês': [100, 150, 120, 130, 140],
        'Português': [80, 100, 95, 90, 110],
        'Alemão': [120, 130, 115, 140, 135],
    }
    df_precos = pd.DataFrame(data_precos)

    # Gerar gráfico de barras com Matplotlib
    ax = df_precos.set_index('País').T.plot(kind='bar', stacked=False, figsize=(10, 6))
    ax.set_ylabel('Preço Médio')
    fig_precos = ax.get_figure()

    # ---------------------------------
    # 3. Distribuição de Alunos por Área de Estudo ou Tipo de Curso
    # ---------------------------------
    labels = ['Tecnologia', 'Negócios', 'Saúde', 'Arte', 'Ciência']
    sizes = [40, 25, 15, 10, 10]

    fig_pizza, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    # Salvar o gráfico do pie chart como uma imagem e codificá-lo em base64
    img_io = io.BytesIO()
    FigureCanvas(fig_pizza).print_png(img_io)
    img_io.seek(0)
    pie_chart_img = base64.b64encode(img_io.getvalue()).decode('utf8')

    # ---------------------------------
    # 4. Mapa Interativo de Popularidade de Cursos por País
    # ---------------------------------
    data_mapa = {
        'País': ['Brasil', 'EUA', 'Alemanha', 'França', 'Reino Unido'],
        'Popularidade': [60, 85, 70, 50, 65],
        'Latitude': [-14.2350, 37.0902, 51.1657, 46.6034, 51.5074],
        'Longitude': [-51.9253, -95.7129, 10.4515, 1.8883, -0.1278],
    }

    df_mapa = pd.DataFrame(data_mapa)

    fig_mapa = px.scatter_geo(df_mapa, lat='Latitude', lon='Longitude', color='Popularidade',
                              size='Popularidade', hover_name='País', projection="natural earth",
                              title="Popularidade de Cursos por País")

    # Passar os gráficos para o HTML
    return render_template('Grafico.html',
                           plot_popularidade=fig_popularidade.to_html(full_html=False),
                           plot_precos=fig_precos,
                           plot_pizza=pie_chart_img,
                           plot_mapa=fig_mapa.to_html(full_html=False))

if __name__ == '__main__':
    app.run(debug=True)
