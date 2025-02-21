import dash
from dash import dcc
from dash import html
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
        self.dados['diaSemana'] = self.dados['data'].dt.weekday
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
    
    #gráfico de pizza para vendas por região
    def analiseVendasRegiao(self, regioesFiltradas):
        dfregiao = self.dados[self.dados['regiao'].isin(regioesFiltradas)]
        dfregiao = dfregiao.groupby(['regiao'])['valor'].sum().reset_index().sort_values(by='valor', ascending=False)
        fig = px.pie(
            dfregiao,
            names= 'regiao',
            values= 'valor',
            title= "Vendas por Região",
            color= "valor"
        )
        return fig
    
    #grafico de vendas mensais
    def analiseVendasMensais(self, anosFiltrados):
        dfMes = self.dados[self.dados['ano'] == anosFiltrados]
        dfMes = dfMes.groupby(['mes','ano'])['valor'].sum().reset_index()
        fig = px.line(
            dfMes,
            x= 'mes',
            y= 'valor',
            color= 'ano',
            title= f'Vendas por Mês - {anosFiltrados}',
            markers= True,
            line_shape= 'spline'
        )
        return fig
    
    #grafico vendas diárias
    def analiseVendasDiarias(self, stard_date, end_date):
        dfDia = self.dados[(self.dados['data'] >= stard_date) & (self.dados['data'] <= end_date)]
        dfDia = dfDia.groupby('data')['valor'].sum().reset_index()
        fig = px.line(
            dfDia,
            x= 'data',
            y= 'valor',
            title= f'Vendas Diárias',
            markers= True,
            #line_shape= 'spline'
        )
        return fig
    
    #frafico vendas semanais
    def analiseVendasSemanais(self):
        dfDiaSemana = self.dados.groupby('diaSemana')['valor'].sum().reset_index()
        dfDiaSemana['diaSemana'] = dfDiaSemana['diaSemana'].map({
            0: 'Domingo',
            1: 'Segunda',
            2: 'Terça',
            3: 'Quarta',
            4: 'Quinta',
            5: 'Sexta',
            6: 'Sábado'
        })
        fig = px.bar(
            dfDiaSemana,
            x= 'diaSemana',
            y= 'valor',
            title= 'Vendas por Dia da Semana',
            color= 'valor'
        )
        lkstyle={'color':'white','text-align':'center'}
        return fig

##identifica os outlines com base em um intervalo
    def analiseOutliers(self):
        q1 = self.dados['valor'].quantile(0.25)
        q3 = self.dados['valor'].quantile(0.75)
        iqr = q3 - q1
        limInf = q1 - 1.5 * iqr
        limSup = q3 + 1.5 * iqr
        outliners = self.dados[(self.dados['valor'] < limInf) | (self.dados['valor'] > limSup)]
        fig = px.scatter(
            outliners,
            x= 'data',
            y= 'valor',
            title= 'Outliers',
        )
        return fig

    #retorna o grafico de distribuição de vendas usando o plotly
    def distVendas(self):
        fig = px.histogram(
            self.dados,
            x= 'valor',
            title= 'Distribuição de Vendas',
            nbins= 30
        )
        return fig

    #calculo de media e desvio pdrão das vendas
    def analiseMediaDesvio(self):
        med = self.dados['valor'].mean()
        desv = self.dados['valor'].std() #calcula o desvio padrão
        return med, desv

    #vendas acumuladas
    def vendasAcumuladas(self):
        dfAcumulado = self.dados.groupby('data')['valor'].sum().cumsum().reset_index()
        dfAcumulado['mediaMovel7']= dfAcumulado['valor'].rolling(window=7).mean()
        dfAcumulado['desvioPadrao7']= dfAcumulado['valor'].rolling(window=7).std()
        dfAcumulado['crescimentoPercentual']= dfAcumulado['valor'].pct_change() * 100
        dfAcumulado['max_valor']= dfAcumulado['valor'].expanding().max()
        dfAcumulado['min_valor']= dfAcumulado['valor'].expanding().min()
        #cria o grafico
        fig = px.line(
            dfAcumulado,
            x= 'data',
            y= ['valor','mediaMovel7','max_valor','min_valor'],
            title= 'Vendas Acumuladas',
            labels= {'valor':'Vendas Acumuladas','mediaMovel7':'Média Móvel 7 dias','max_valor':'Máximo','min_valor':'Mínimo'},
            markers= True
        )
        fig.add_trace(
            go.Scatter(
                x= dfAcumulado['data'],
                y= dfAcumulado['crescimentoPercentual'],
                mode= 'lines',
                name= 'Crescimento Percentual',
                line= dict(color='orange', width=2, dash='dot'),
                yaxis= 'y2'
            )
        )
        fig.update_layout(
            title_font=dict(size=20, family='Poppins', color='#2980b9'),
            plot_bgcolor= '#34495e',
            paper_bgcolor= '#2c3e50',
            font= dict(color='#ecf0f1', family='Roboto'),
            xaxis=dict(
                title= 'Data',
                tickformat= '%d/%m/%Y',
                showgrid= True,
                gridcolor= '#7f8c8d',
                tickangle= 45
            ),
            yaxis= dict(
                title= 'Vendas Acumuladas',
                showgrid= True,
                gridcolor= '#7f8c8d',
            ),
            yaxis2= dict(
                title= 'Crescimento Percentual (%)',
                showgrid= True,
                side = 'right',
                overlaying= 'y',
                tickformat= '.1f'
            ),
            legend= dict(
                title= 'Métricas',
                orientation= 'h',
                yanchor= 'bottom',
                y= 1.01,
                xanchor= 'center',
                x= 0.5
            )
        )
        return fig

#------------------- Instanciar o objeto de analise de vendas-------------------#
analise = AnalisadorDeVendas(df)
#------------------- layout do app dash -------------------#
app.layout = html.Div([ 
    html.H1('Análise de Vendas', style={'color':'white','text-align':'center'}),
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
            options=[
                    {"label": str(ano), "value": ano} for ano in df["ano"].unique()
                    ],
                    value=df["ano"].min(),
                    style={"width": "48%"},
                ),

            
        html.Label('Selecione um periodo'),
        dcc.DatePickerRange(
            id = 'date-picker-range',
            start_date = df['data'].min().date(),
            end_date = df['data'].max().date(),
            display_format = 'YYYY-MM-DD',
            style = {'width':'48%'}
        ),
    ], style={'background':'black','padding':'20px'}),
    #grafico
    html.Div([
        dcc.Graph(id='grafico-produto'),
        dcc.Graph(id='grafico-regiao'),
        dcc.Graph(id='grafico-ano'),
        dcc.Graph(id='grafico-dia'),
        dcc.Graph(id='grafico-semana'),
        dcc.Graph(id='grafico-outliers'),
        dcc.Graph(id='grafico-distribuicao'),
        dcc.Graph(id='grafico-mediaDesvio'),
        dcc.Graph(id='grafico-vendasAcumulado')
    ])
        
],style={'background':'black','padding':'20px'})

#------------------- Callbacks -------------------#
@app.callback(
    Output('grafico-produto', 'figure'),
    Output('grafico-regiao', 'figure'),
    Output('grafico-ano', 'figure'),
    Output('grafico-dia', 'figure'),
    Output('grafico-semana', 'figure'),
    Output('grafico-outliers', 'figure'),
    Output('grafico-distribuicao', 'figure'),
    Output('grafico-mediaDesvio', 'figure'),
    Output('grafico-vendasAcumulado', 'figure'),
    [
        Input('produto-dropdown', 'value'),
        Input('regiao-dropdown', 'value'),
        Input('ano-dropdown', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ]
)
def upgrade_graphs(produtos, regioes, anos, start_date, end_date):
    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        figRegiao = analise.analiseVendasRegiao(regioes)
        figProduto = analise.analiseVendasProduto(produtos)
        figMes = analise.analiseVendasMensais(anos)
        figDia = analise.analiseVendasDiarias(start_date, end_date)
        figSemana = analise.analiseVendasSemanais()
        figOutliers = analise.analiseOutliers()
        figDistribuicao = analise.distVendas()
        figvendasAcumuladas = analise.vendasAcumuladas()
        media, desvio = analise.analiseMediaDesvio()
        figMediaDesvio = go.Figure([
            go.Bar(
                x=['Média', 'Desvio Padrão'],
                y=[media, desvio],
                marker_color=['blue', 'red']
            )
        ], layout=go.Layout(title=f'Média e Desvio padrão: Média ={media:.2f}, Desvio={desvio:.2f}'))

        return (figProduto, figRegiao, figMes, figDia, figSemana, figOutliers, figDistribuicao, figMediaDesvio, figvendasAcumuladas)
    except Exception as e:
        print(f'Erro ao atualizar os graficos: {str(e)}')
        return go.Figure()

# roda o app
if __name__ == '__main__':
    app.run_server(debug=True)