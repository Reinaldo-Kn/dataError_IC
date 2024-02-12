import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np


def temp_geral(data_escolhida):
    df = pd.read_csv('DUSTAINEW.csv', sep=';', decimal=',')
    df['Datetime'] = pd.to_datetime(df['Datetime'])  

    df = df[df['Datetime'].dt.date == data_escolhida]
    
    temperatura_column = df['Temperatura']
    horas = df['Datetime']
    horas = horas.dt.strftime('%H:%M')
    
    min_datetime = min(df['Datetime'])
    max_datetime = max(df['Datetime'])
   
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=45))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set(xlabel='Horas', ylabel='Temperatura', title='Temperatura Geral', xlim=[min_datetime, max_datetime])
    ax.plot(df['Datetime'], temperatura_column, label='Temperatura', linewidth=2, color='blue')
    ax.grid(True)
    fig.autofmt_xdate()

    plt.show()


def temp_outliers(data_escolhida):
    df = pd.read_csv('DUSTAINEW.csv', sep=';', decimal=',')
    df['Datetime'] = pd.to_datetime(df['Datetime'])  

    df = df[df['Datetime'].dt.date == data_escolhida]
    
    temperatura_column = df['Temperatura']
    horas = df['Datetime']
    horas = horas.dt.strftime('%H:%M')
    
    min_datetime = min(df['Datetime'])
    max_datetime = max(df['Datetime'])
    
    Q1 = temperatura_column.quantile(0.25)
    Q3 = temperatura_column.quantile(0.75)
    IQR = Q3 - Q1

    threshold = 2
    lower_limit = Q1 - threshold * IQR
    upper_limit = Q3 + threshold * IQR

    outliers = df[(df['Temperatura'] < lower_limit) | (df['Temperatura'] > upper_limit)]
        
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=45))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set(xlabel='Horas', ylabel='Temperatura', title='Temperatura com Outliers', xlim=[min_datetime, max_datetime])
    ax.plot(df['Datetime'], temperatura_column, label='Temperatura', linewidth=2, color='blue')
    ax.scatter(list(outliers['Datetime']), list(outliers['Temperatura']), color='red', label='Outliers', zorder=5)
    ax.grid(True)
    fig.autofmt_xdate()
    plt.legend()
    plt.show()
    
    print(IQR)
    print(Q1)
    print(Q3)
    print(df['Temperatura'].describe())

def temp_peak(data_escolhida):
    df = pd.read_csv('DUSTAI.csv', sep=';', decimal=',', parse_dates=['Data'])
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.hour
    df = df.set_index('Data')
    
    # Filtrando os dados para a data escolhida
    df = df[df.index.date == data_escolhida]
    
    temperatura_column = df['Temperatura']
    horas = df['Hora']
    
    mean_temp = temperatura_column.mean()
    std_temp = temperatura_column.std()
    spike_threshold = 2 #aumentar para 2 ou 3 

    spike_errors = temperatura_column[abs(temperatura_column - mean_temp) > spike_threshold * std_temp]
    plt.figure(figsize=(10, 6))
    plt.plot(horas, temperatura_column, label='Temperatura')
    plt.scatter(spike_errors.index, spike_errors, color='red', label='Picos de Erros')
    plt.axhline(y=mean_temp, color='green', linestyle='--', label=f'Média: {mean_temp:.2f}')
    plt.axhline(y=mean_temp + spike_threshold * std_temp, color='orange', linestyle='--', label=f' Desvios padrão: {spike_threshold}')
    plt.axhline(y=mean_temp - spike_threshold * std_temp, color='orange', linestyle='--')
    plt.title('Temperatura com Picos de Erros')
    plt.xlabel('Data')
    plt.ylabel('Temperatura')
    plt.legend()
    plt.show()
    

def temp_stuck(data_escolhida):
    df = pd.read_csv('DUSTAI.csv', sep=';', decimal=',', parse_dates=['Data'])
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.hour
    df = df.set_index('Data')
    
    # Filtrando os dados para a data escolhida
    df = df[df.index.date == data_escolhida]
    
    temperatura_column = df['Temperatura']
    horas = df['Hora']
    resultados = []     
    tamanho_sequencia = 30
    threshold_variancia = 0.25

    for i in range(len(df) - tamanho_sequencia + 1):
        sequencia = df['Temperatura'].iloc[i:i+tamanho_sequencia]
        media_sequencia = round(sequencia.mean(), 2)
        variancia_sequencia = round(sequencia.var(), 2)

        if variancia_sequencia <= threshold_variancia:
            if all(media_sequencia - threshold_variancia <= valor <= media_sequencia + threshold_variancia for valor in sequencia):
                id_correspondente = df['Num'].iloc[i]
                resultados.append((id_correspondente, media_sequencia))
      
    df_resultados = pd.DataFrame(resultados, columns=['ID', 'Temperatura'])
    plt.bar(df_resultados['ID'], df_resultados['Temperatura'])
    plt.xlabel('ID')
    plt.ylabel('Temperatura Stuck')
    plt.title('Historiograma das Temperaturas Stuck')
    plt.show()
    return resultados

def temp_variance(data_escolhida):
    df = pd.read_csv('DUSTAI.csv', sep=';', decimal=',')
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, infer_datetime_format=True)
    df = df.set_index('Data')  
    temperatura_column = df[df.index.date == data_escolhida]['Temperatura']
    
    id_correspondente = df['Num']
    threshold = 5
    vetor_ids = []

    for i in range(len(df) - 1):
        temperatura_atual = df.iloc[i]['Temperatura']
        temperatura_proxima = df.iloc[i + 1]['Temperatura']

        diff = abs(temperatura_proxima - temperatura_atual)

        if diff > threshold:
            vetor_ids.append(id_correspondente.iloc[i])
        
    
    if vetor_ids == []:
            print('Não há valores com variação maior que 5 graus')
    return vetor_ids
     


if __name__ == '__main__':
    while True:
        print('Escolha uma das opções abaixo:')
        print('1. Temperatura Geral')
        print('2. Temperatura com Outliers')
        print('3. Temperatura com Picos de Erros')
        print('4. Temperatura com Valores Stuck')
        print('5. Temperatura com Variância')
        print('6. Sair')
        opcao = int(input('Digite a opção desejada: '))
        if opcao == 1:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            temp_geral(pd.to_datetime(data_escolhida, dayfirst=True).date())
        elif opcao == 2:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            temp_outliers(pd.to_datetime(data_escolhida, dayfirst=True).date())
        elif opcao == 3:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            temp_peak(pd.to_datetime(data_escolhida, dayfirst=True).date())
        elif opcao == 4:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            resultados = temp_stuck(pd.to_datetime(data_escolhida, dayfirst=True).date())
            print(resultados)
                
        elif opcao == 5:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            resultados = temp_variance(pd.to_datetime(data_escolhida, dayfirst=True).date())
            print(resultados)
            
        elif opcao == 6:
            break
        else:
            print('Opção inválida!')
    