import pandas as pd
import random
from datetime import datetime, timedelta
import os

os.chdir(os.path.dirname(__file__))

#fundção para gerar dados
def gerarDadosVendas(numLinhas):
    produtosLista = ['Produto A', 'Produto B', 'Produto C', 'Produto D']
    regiaoLista = ['Nordeste','Sudeste','Sul','Norte','Oeste']
    dados = []
    for _ in range(numLinhas):
        produto = random.choice(produtosLista)
        regiao = random.choice(regiaoLista)
        valor = round(random.uniform(50,500),2)
        data = datetime.today() - timedelta(days=random.randint(0,365))
        dados.append([produto,regiao,valor,data])
    return dados

dadosVendas = gerarDadosVendas(100)

dfVendas = pd.DataFrame(dadosVendas, columns=['produto','regiao','valor','data'])

dfVendas.to_csv('vendas.csv', index=False)

print("Arquivo criado com sucesso!")
