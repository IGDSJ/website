import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os
from pymongo import MongoClient

def insercao(file,documento):
    folder = '/website/uploads/'
    dataset = pd.read_csv(folder+file)
    documento.insert_many(dataset.to_dict('records'))

def criar_relatorio(file, modo, tempo,grandeza,placa):
    folder = '/website/uploads/'
    data = pd.read_csv(folder+file)
    data['DATE_TIME'] = pd.to_datetime(data['DATE_TIME'])
    
    datetime_str = str(tempo)                                                     #Date in string
    if modo =='mensal':
      date = datetime.strptime(datetime_str,'%Y-%m')                  #Date in datetime (in format %y-%m-%d %H:%M:%S)
      date = date.strftime('%Y-%m')  
      data_teste = data[data['DATE_TIME'].dt.strftime('%Y-%m')==date]             #Datas in the specific year and month
      
    if modo == 'diario':
      date = datetime.strptime(datetime_str,'%Y-%m-%d')                  #Date in datetime (in format %y-%m-%d %H:%M:%S)
      date = date.strftime('%Y-%m-%d')   
      data_teste = data[data['DATE_TIME'].dt.strftime('%Y-%m-%d')==date]          #Datas in the specific year,month and day
      
    if modo == 'horario':
      date = datetime.strptime(datetime_str,'%Y-%m-%d %H')                  #Date in datetime (in format %y-%m-%d %H:%M:%S)
      date = date.strftime('%Y-%m-%d %H')  
      data_teste = data[data['DATE_TIME'].dt.strftime('%Y-%m-%d %H')==date]       #Datas in the specific year, month, day and hour
      
    if modo == 'total':
      data_teste = data
      date = 'Total'
    if placa =='todas':
        data_teste = data_teste
    else:
      data_teste = data_teste[data_teste['SOURCE_KEY']==placa]
    fig = plt.figure(figsize=(30,20))
    ax = fig.add_subplot(1, 1, 1)
    
    ax.plot(data_teste['DATE_TIME'].values,data_teste[str(grandeza)].values,label=str(date))
    ax.legend(loc='upper left')
    ax.set_title("{} {}".format(str(grandeza),modo))
    ax.set_xlabel('Time')
    ax.set_ylabel(str(grandeza))
    
    if os.path.exists('/website/imagens/{}_{}.pdf'.format(str(grandeza),modo)):
        os.remove('/website/imagens/{}_{}.pdf'.format(str(grandeza),modo))
    
    plt.savefig('/website/imagens/{}_{}_{}.pdf'.format(str(grandeza),placa,tempo), format='pdf')
      
client = MongoClient('localhost', 27017)
banco = client.teste_insercao2
aluno = banco.aluno

import pprint


teste = pprint.pprint(banco.aluno.find_one())

teste = banco.aluno.count_documents({})