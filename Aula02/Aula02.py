import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

dados_conceitos ={ # dicionarios com AS INFORMAÇÕES DA CAIXA DROPDOWN
    'java' :   {'variaves':8,'condicionais':10 , 'loops' : 4 , 'poo':3 ,'funções':4},
    'python' : {'variaves':9,'condicionais':7 , 'loops' : 8 , 'poo':4 ,'funções':5},
    'sql' :    {'variaves':7,'condicionais':10 , 'loops' : 9 , 'poo':8 ,'funções':4},
    'golang' : {'variaves':10,'condicionais':5, 'loops' : 8 , 'poo':4 ,'funções':3},
    'javascript' : {'variaves':9,'condicionais':7, 'loops' : 5 , 'poo':6 ,'funções':8}
}

cores_map=dict(
    java='red',
    python='green',
    sql='yellow',
    golang='blue',
    javascript='pink'
)



app = dash.Dash(__name__)

app.layout = html.Div([
    html.H4(
        'Sebrae Maranhao', 
        style={'textAlign':'center'}
    ),

    html.Div(
        dcc.Dropdown(
            id='dropdown_linguagens',
            options=[
                {'label':'Java','value':'java'},
                {'label':'Python','value':'python'},
                {'label':'SQL','value':'sql'},
                {'label':'GoLang','value':'golang'},
                {'label':'JavaScript','value':'javascript'}
            ],
            value=['java'],
            multi=True,
            style={'width' : '50%', 'margin' : '0 auto'}
        )
    ),

    dcc.Graph(id='grafico_linguagem')
], style={'width' : '80%',
         'margin': '0 auto'}

)

@app.callback( # uma funcao que vai ser chamada atraves de um evento
    Output('grafico_linguagem', 'figure'),
    [Input('dropdown_linguagens','value')]
    
) 

def scarter_linguagens(linguagens_selecionadas):
    scarter_trace=[]

    for linguagem in linguagens_selecionadas:
        dados_linguagem= dados_conceitos[linguagem]
        for conceito, conhecimento in dados_linguagem.items():
            scarter_trace.append(
                go.Scatter(
                    x=[conceito],
                    y=[conhecimento],
                    mode='markers',
                    name=linguagem.title(),
                    marker={'size':15 , 'color':cores_map[linguagem]},
                    showlegend=False
                    
                )
                
            )
    scartter_layout =go.Layout(
        title="Meus conhecimentos em Linguagens",
        xaxis=dict(title ='Conceitos', showgrid=False),
        yaxis=dict(title ='Niveis de conhecmento', showgrid=False)
    )

    return {'data': scarter_trace,'layout':scartter_layout}

if __name__  == '__main__':
    app.run_server(debug=True)