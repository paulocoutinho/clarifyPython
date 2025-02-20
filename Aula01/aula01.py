import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot

import seaborn as sns
import datetime as dt

from IPython.display import display


#links da tabelas csv
dfNY = pd.read_csv("https://www.dropbox.com/s/8i2nw6bd5ha7vny/listingsNY.csv?dl=1")
dfRJ = pd.read_csv("https://www.dropbox.com/s/yyg8hso7fbjf1ft/listingsRJ.csv?dl=1")

"""
id: identificação de cada imovel
hot_id: o numero de identificação do anfitrião
neighboarhood_group: conjunto de grupo de bairros
latitude - coordenada latitude
longitude: coordenada longitude
room_type: o top de quarto
price: valor da pernoite do imovel
minimun_nights: noites minimas para locação
numer_of_reviews: numero de avaliações
last_review: data da ultima avaliação
reviews_per_month: quantidade de avaliações por mês
calculated_host_listing_count: quantidade de imoveis do mesmo anfitrião
availability_365: dias que o anuncio esta disponivel/ano
number_reviews_ltm:avaliações nos ultimos 12 meses
license: nunhum valor valido

"""
print ("\n#################### INICIO ####################")
print ("\n----------------------------")
print ("\nDataFram NY:") #imprime o datafram 
display(dfNY.all)
dfNY['last_review'] = pd.to_datetime(dfNY['last_review'], format="%Y-%m-%d") #preenchendo a variavel ultimo review
print(dfNY['last_review'])
print(f'New York \nEntradas:{dfNY.shape[0]}\nVariaveis:{dfNY.shape[1]}\n')
display(dfNY.dtypes)

dfNY['year'] = dfNY['last_review'].dt.year

#calcula o valor do dollar
dfNY['price'] =  dfNY['price'].mask(dfNY['year'] <= 2011,(dfNY['price'] / 1.674))

variaveis = ['id',
             'name',
             'host_id',
             'host_name',
             'neighbourhood_group',
             'neighbourhood',
             'latitude',
             'longitude',
             'room_type',
             'price',
             'minimum_nights',
             'number_of_reviews',
             'last_review',
             'reviews_per_month',
             'calculated_host_listings_count',
             'availability_365',
             'number_of_reviews_ltm',
             'license'
]
vz = []
dado = []

#for para preencher as variaveis
for i in variaveis:
   dado.append(dfNY[i].isnull().sum() / dfNY[i].shape[0])
   dado.append(dfRJ[i].isnull().sum() / dfRJ[i].shape[0])
   vz.append(dado[:])
   dado.clear()
vz

#construindo uma tabela com duas tabelas New York e Rio de Janeiro
pd.DataFrame(vz, columns=['New York', 'Rio de Janeiro'], index=variaveis)

#Gera um gafico com os dados
#dropbna (linhas que não vai ser usado)

dfNY_clean = dfNY.dropna(subset=['name', 'host_name'], axis=0)
dfRJ_clean = dfRJ.dropna(subset=['name', 'host_name'], axis=0)

#calcula a média dos valores
rpm_ny_median = dfNY_clean.reviews_per_month.median()
dfNY_clean = dfNY_clean.fillna({'reviews_per_month': rpm_ny_median})

rpm_ny_median = dfRJ_clean.reviews_per_month.median()
dfNY_clean = dfRJ_clean.fillna({'reviews_per_month': rpm_ny_median})

lr_ny_median = dfNY_clean['last_review'].astype('datetime64[ns]').quantile(0.5,interpolation="midpoint")
lr_ny_median = dfRJ_clean['last_review'].astype('datetime64[ns]').quantile(0.5,interpolation="midpoint")
#substitui o valor calculado do last_review pela interpolação
dfNY_clean = dfNY_clean.fillna({'last_review': rpm_ny_median})
dfNY_clean = dfRJ_clean.fillna({'last_review': rpm_ny_median})

#montando uma tabela exemplo com preços e noites minimas
dx0 = ['price','minimum_nights']

#alimentando a tabela
for n in dx0:
  data_a = dfNY_clean[n]
  data_b = dfRJ_clean[n]
  data_2d = [data_a, data_b]
  plt.boxplot(data_2d, vert = False, labels=["New York", "Rio de Janeiro"])
  plt.title(n)
#mostra o grafico
plt.show () 

#imprimindo tabela
dfNY_clean[['price','minimum_nights','number_of_reviews','reviews_per_month','calculated_host_listings_count','availability_365']].describe()
dfRJ_clean[['price','minimum_nights','number_of_reviews','reviews_per_month','calculated_host_listings_count','availability_365']].describe()

dfNY_out = dfNY_clean.copy()
dfNY_out.drop(dfNY_out[dfNY_out.price > 1100].index, axis=0, inplace=True)
dfNY_out.drop(dfNY_out[dfNY_out.minimum_nights > 66].index, axis=0, inplace=True)

dfRJ_out = dfRJ_clean.copy()
dfRJ_out.drop(dfRJ_out[dfRJ_out.price > 600].index, axis=0, inplace=True)
dfRJ_out.drop(dfRJ_out[dfRJ_out.minimum_nights > 4].index, axis=0, inplace=True)

#criando tabela
var = [ 'Entire home/apt',
        'Private room',
        'Shared room',
        'Hotel room'
]

dado_var = {}

for i in var:
  dado_var[i] = [dfNY_out.loc[dfNY_out.room_type == i].shape[0] / dfRJ_out.room_type.shape[0],dfRJ_out.loc[dfRJ_out.room_type == i].shape[0] / dfRJ_out.room_type.shape[0]]

ima = pd.DataFrame(dado_var, index=['New York','Rio de Janeiro'])
ima.plot(kind='barh', stacked=True,figsize=(6,4), color=['green','white','red','orange'])
plt.legend(loc="lower left", bbox_to_anchor=(0.8,1.0))
plt.show()


# print ("\n")
# print ("\n#################### INICIO ####################")
# print ("\n----------------------------")
# print ("\nDataFram RJ:")
# display(dfRJ.all)
# print (f'Rio de Janeiro:{dfRJ.shape[0]}\nVariaveis:{dfRJ.shape[1]}\n')
# display(dfRJ.dtypes)