import pandas as pd
import random
from datetime import datetime, timedelta
import os

os.chdir(os.path.dirname(__file__))

#fundção para gerar dados
def gerarDadosVendas(numLinhas):
    produtos = ["Produto A","Produto B","Produto C","Produto D"]
    regiao = ["Nordeste","Sudeste","Sul","Norte","Centro-Oeste"]
    dados = []
    
    for aux in range(numLinhas):
        produtos = random.choice(produtos)
        regiao = random.choice(regiao)
        valor = round(random.uniform(50,500),2)
        data = datetime.today() - timedelta(days=random.randint(0,365))
        dados.append([produtos,regiao,valor,data])
    return dados

dadosVendas = gerarDadosVendas(100)

dfVendas = pd.DataFrame(dadosVendas, columns=['Produtos','Região','Valor','Data'])

dfVendas.to_csv('vendas.csv', index=False)

print("Arquivo criado com sucesso!")
