import dash
import dash_core_components as dcc
import dash_html_components as html 
from matplotlib import figure, layout_engine
import plotly.graph_objs as go
from dash.dependencies import Input, Output 

class DashApp:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.layout = self.create_layout()
        self.app.layout = self.layout
        self.create_callbacks()

    def create_layout(self):
        layout = html.Div([
            html.H1("Exemplo de Gráfico Interatico com Plotly e Dash"),

            dcc.Graph(
                id='graficoInterativo',
                figure=self.create_figure()
            )
        ])
        return layout   
    
    def create_figure(self):
        x = [1,2,3,4,5]
        y = [10,11,12,13,14]
        
        figure ={
            'data':[
                go.Scatter(
                    x=x,
                    y=y,
                    mode='lines+markers',
                    name='Linha de Exemplo'
                )
            ],
            'layout': go.Layout(
                title='Gráfico Interativo',
                xaxis={'title':'Eixo X'},
                yaxis={'title':'Eixo Y'},
                
            )
        }
        return figure
    
    def create_callbacks(self):
        @self.app.callback(
            Output('graficoInterativo','figure'),
            [Input('graficoInterativo','relayoutData')]
        )
        def updateGraph(inputData):
            return self.create_figure()
    
    def run(self):
        self.app.run_server(debug=True)

if __name__ == '__main__':
    app = DashApp()
    app.run()