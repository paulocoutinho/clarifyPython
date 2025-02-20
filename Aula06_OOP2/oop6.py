import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
import base64
import os

os.chdir(os.path.dirname(__file__))

#inicializando o app dash
app = dash.Dash(__name__)
#carrega para o dataset os dados de vendas
df = pd.read_csv('vendas.csv')
#cria a classe para a estrutura de analise de dados
class AnalisadorDeVendas:
    def __init__ (self,dados):
        #inicializa a classe com o dataframe da tabela vendas
        self.dados = dados
        self.limparDados()

    def limparDados(self):
        #limpeza e preparação dos dados para analise com as demais funções
        self.dados['data'] = pd.to_datetime(self.dados['data'],errors='coerce')#converte as data em formato de texto para o formato datetime
        self.dados['valor'] = self.dados['valor'].replace({',': '.'}, regex=True).astype(float)
        self.dados['mes'] = self.dados['data'].dt.month
        self.dados['ano'] = self.dados['data'].dt.year
        self.dados['dia'] = self.dados['data'].dt.day
        self.dados['dia_da_semana'] = self.dados['data'].dt.weekday
        #remove os dados ausentes em colunas
        self.dados.dropna(subset=['produto','valor'], inplace=True)
    
    def analiseVendasProduto(self, produtosFiltrados):
        dfproduto = self.dados[self.dados['produto'].isin(produtosFiltrados)]
        dfproduto = dfproduto.groupby(['produto'])['valor'].sum().reset_index().sort_values(by='valor', ascending=True)
        fig = px.bar(
            dfproduto,
            x= 'produto',
            y= 'valor',
            title= "Vendas por Produto",
            color= "valor"
        )
        return fig

#------------------- Instanciar o objeto de analise de vendas-------------------#
analise = AnalisadorDeVendas(df)
#------------------- layout do app dash -------------------#
app.layout = html.Div([
    html.H1('Análise de Vendas', style={'text-align':'center'}),
    #cria os filtros de seleção para o painel
    html.Div([
        html.Label('Selecione os produtos'),
        dcc.Dropdown(
            id = 'produto-dropdown',
            options = [{'label':produto, 'value':produto} for produto in df['produto'].unique()],
            multi = True,
            value = df['produto'].unique().tolist(),
            style = {'width':'48%'}
        ),
        html.Label('Selecione as Rigões'),
        dcc.Dropdown(
            id = 'regiao-dropdown',
            options = [{'label':regiao, 'value':regiao} for regiao in df['regiao'].unique()],
            multi = True,
            value = df['regiao'].unique().tolist(),
            style = {'width':'48%'}
        ),
        html.Label('Selecione as Ano'),
        dcc.Dropdown(
            id = 'ano-dropdown',
            options = [{'label':str(ano), 'value':ano} for ano in df['ano'].unique()],
            value = df['ano'].min(),
            style = {'width':'48%'}
        ),
        html.Label('Selecione um periodo'),
        dcc.DatePickerRange(
            id = 'date-picker-range',
            start_date = df['data'].min().date(),
            end_date = df['data'].max().date(),
            display_format = 'YYYY-MM-DD',
            style = {'width':'48%'}
        ),
    ], style={'padding':'20px'}),
    html.Div([
        dcc.Graph(id='grafico-produto')
    ])
        
])

#------------------- Callbacks -------------------#
@app.callback(
    Output('grafico-produto', 'figure'),
    [Input('produto-dropdown', 'value'), Input('regiao-dropdown', 'value'), Input('ano-dropdown', 'value'), Input('date-picker-range', 'start_date'), Input('date-picker-range', 'end_date')] 
)
def upgrade_graphs(produtos, regioes, anos, start_date, end_date): 
    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        figProduto = analise.analiseVendasProduto(produtos)
        
        return figProduto
    
    except Exception as e:
        print(f'Erro ao atualizar os graficos: {str(e)}')
        return go.Figure()
        

#roda o app
if __name__ == '__main__':
    app.run_server(debug=True)