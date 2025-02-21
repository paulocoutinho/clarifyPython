import dash
from dash import dcc, html
import requests
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

# função para consultar a API e retornar dados
def consultaNomes():
    url = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/paulo|bruno|felipe|guilherme"

    response = requests.get(url)
    dados = response.json()
    nomes = []  # Initialize nomes outside the loop, so it will be a local variable.

    for nomeData in dados:
        nome = nomeData['nome']

        for res in nomeData['res']:
            periodo = res['periodo']
            frequencia = res['frequencia']
            nomes.append({'Nome': nomeData['nome'], 'Periodo': periodo, 'Frequencia': frequencia}) 
    df = pd.DataFrame(nomes) 
    return df

def criarGrafico(df):
    fig = px.line(df,
                  x='Periodo',  
                  y='Frequencia',  
                  color='Nome',
                  title='Frequência dos Nomes ao Longo dos Períodos',
                  labels={'Periodo': 'Período', 'Frequencia': 'Frequência'}  
                  )
    return fig

app.layout = html.Div([
    html.H1("Frequência de Nomes ao longo dos Períodos"),
    dcc.Graph(
        id='grafico',
        figure=criarGrafico(consultaNomes())
    )
])

# rodando o app
if __name__ == "__main__":
    app.run_server(debug=True)
