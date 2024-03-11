import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from scipy.stats import t
import scikit_posthocs as sp
def temp_geral(data_escolhida,coluna_escolhida):
    df = pd.read_csv('DUSTAINEW.csv', sep=';', decimal=',')
    df['Datetime'] = pd.to_datetime(df['Datetime'])  

    df = df[df['Datetime'].dt.date == data_escolhida]
    
    temperatura_column = df[coluna_escolhida]
    horas = df['Datetime']
    horas = horas.dt.strftime('%H:%M')
    
    min_datetime = min(df['Datetime'])
    max_datetime = max(df['Datetime'])
   
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=45))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set(xlabel='Horas', ylabel=coluna_escolhida, title=f'{coluna_escolhida} Geral', xlim=[min_datetime, max_datetime])
    ax.plot(df['Datetime'], temperatura_column, label=coluna_escolhida, linewidth=2, color='blue')
    ax.grid(True)
    fig.autofmt_xdate()
    plt.show()


def temp_outliers(data_escolhida, coluna_escolhida):
    df = pd.read_csv('DUSTAINEW.csv', sep=';', decimal=',')
    df['Datetime'] = pd.to_datetime(df['Datetime'])  

    df = df[df['Datetime'].dt.date == data_escolhida]
    
    temperatura_column = df[coluna_escolhida]  
    horas = df['Datetime']
    horas = horas.dt.strftime('%H:%M')
    
    min_datetime = min(df['Datetime'])
    max_datetime = max(df['Datetime'])
    
    Q1 = temperatura_column.quantile(0.25)
    Q3 = temperatura_column.quantile(0.75)
    IQR = Q3 - Q1

    threshold = 1.5
    
    lower_limit = Q1 - threshold * IQR
    upper_limit = Q3 + threshold * IQR

    outliers = df[(temperatura_column < lower_limit) | (temperatura_column > upper_limit)]  # Use a coluna escolhida
        
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=45))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set(xlabel='Horas', ylabel=coluna_escolhida, title=f'{coluna_escolhida} com Outliers', xlim=[min_datetime, max_datetime])
    ax.plot(df['Datetime'], temperatura_column, label=coluna_escolhida, linewidth=2, color='blue')
    ax.scatter(list(outliers['Datetime']), list(outliers[coluna_escolhida]), color='red', label='Outliers', zorder=5)
    ax.grid(True)
    fig.autofmt_xdate()
    plt.legend()
    plt.show()
    
    print(IQR)
    print(Q1)
    print(Q3)
    print(temperatura_column.describe())

def temp_outlier_3sigma(data_escolhida, coluna_escolhida):
    df = pd.read_csv('DUSTAINEW.csv', sep=';', decimal=',')
    df['Datetime'] = pd.to_datetime(df['Datetime'])  

    df = df[df['Datetime'].dt.date == data_escolhida]
    
    temperatura_column = df[coluna_escolhida]  
    horas = df['Datetime']
    horas = horas.dt.strftime('%H:%M')
    
    min_datetime = min(df['Datetime'])
    max_datetime = max(df['Datetime'])
    
    Upper_limit = temperatura_column.mean() + 3 * temperatura_column.std()
    Lower_limit = temperatura_column.mean() - 3 * temperatura_column.std()
    
    outliers = df[(temperatura_column < Lower_limit) | (temperatura_column > Upper_limit)]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=45))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set(xlabel='Horas', ylabel=coluna_escolhida, title=f'{coluna_escolhida} com Outliers 3 sigma', xlim=[min_datetime, max_datetime])
    ax.plot(df['Datetime'], temperatura_column, label=coluna_escolhida, linewidth=2, color='blue')
    ax.scatter(list(outliers['Datetime']), list(outliers[coluna_escolhida]), color='red', label='Outliers', zorder=5)
    ax.grid(True)
    fig.autofmt_xdate()
    plt.legend()
    plt.show()
    
def temp_peak(data_escolhida, coluna_escolhida):
    df = pd.read_csv('DUSTAINEW.csv', sep=';', decimal=',')
    df['Datetime'] = pd.to_datetime(df['Datetime'])  

    df = df[df['Datetime'].dt.date == data_escolhida]
    
    temperatura_column = df[coluna_escolhida]  
    horas = df['Datetime']
    horas = horas.dt.strftime('%H:%M')
    
    min_datetime = min(df['Datetime'])
    max_datetime = max(df['Datetime'])
    
    mean_temp = temperatura_column.mean()
    std_temp = temperatura_column.std()
    spike_threshold = 2
    
    # Identificar os picos de erro
    spike_errors = df[temperatura_column > (mean_temp + spike_threshold * std_temp)]  # Use a coluna escolhida
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=50))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set(xlabel='Horas', ylabel=coluna_escolhida, title=f'{coluna_escolhida} com Picos de Erros', xlim=[min_datetime, max_datetime])
    ax.plot(df['Datetime'], temperatura_column, label=coluna_escolhida, linewidth=2, color='blue')
    ax.scatter(spike_errors['Datetime'], spike_errors[coluna_escolhida], color='red', label='Picos de Erros')
    ax.axhline(y=mean_temp, color='green', linestyle='--', label=f'Média: {mean_temp:.2f}')
    ax.axhline(y=mean_temp + spike_threshold * std_temp, color='orange', linestyle='--', label=f' Desvios padrão: {spike_threshold}')
    ax.axhline(y=mean_temp - spike_threshold * std_temp, color='orange', linestyle='--')
    ax.grid(True)
    fig.autofmt_xdate()
    plt.legend()
    plt.show()

   

def temp_stuck(data_escolhida, coluna_escolhida):
    df = pd.read_csv('DUSTAINEW.csv', sep=';', decimal=',')
    df['Datetime'] = pd.to_datetime(df['Datetime'])  

    df = df[df['Datetime'].dt.date == data_escolhida]
    
    temperatura_column = df[coluna_escolhida]  
    horas = df['Datetime']
    horas = horas.dt.strftime('%H:%M')

    resultados = []     
    tamanho_sequencia = 25
    threshold_variancia = 0.25

    for i in range(len(df) - tamanho_sequencia + 1):
        sequencia = df[coluna_escolhida].iloc[i:i+tamanho_sequencia]  
        media_sequencia = round(sequencia.mean(), 2)
        variancia_sequencia = round(sequencia.var(), 2)

        if variancia_sequencia <= threshold_variancia:
            if all(media_sequencia - threshold_variancia <= valor <= media_sequencia + threshold_variancia for valor in sequencia):
                id_correspondente = df['Num'].iloc[i]
                resultados.append((id_correspondente, media_sequencia))
      
    df_resultados = pd.DataFrame(resultados, columns=['ID', 'Temperatura'])
    plt.bar(df_resultados['ID'], df_resultados['Temperatura'])
    plt.xlabel('ID')
    plt.ylabel(coluna_escolhida)  
    plt.title(f'Historiograma das {coluna_escolhida} Stuck')  
    plt.show()
    return resultados


def temp_variance(data_escolhida, coluna_escolhida):
    df = pd.read_csv('DUSTAINEW.csv', sep=';', decimal=',')
    df['Datetime'] = pd.to_datetime(df['Datetime'])  

    df = df[df['Datetime'].dt.date == data_escolhida]
    
    temperatura_column = df[coluna_escolhida]  
    horas = df['Datetime']
    horas = horas.dt.strftime('%H:%M')
    
    id_correspondente = df['Num']
    threshold = 5
    vetor_ids = []

    for i in range(len(df) - 1):
        temperatura_atual = df.iloc[i][coluna_escolhida]  
        temperatura_proxima = df.iloc[i + 1][coluna_escolhida]  

        diff = abs(temperatura_proxima - temperatura_atual)

        if diff > threshold:
            vetor_ids.append(id_correspondente.iloc[i])
            print(f'ID: {id_correspondente.iloc[i]} - Variação: {diff:.2f} ')
    
    if not vetor_ids:
        print(f'Não há valores com variação maior que {threshold} graus na coluna {coluna_escolhida}')
    return vetor_ids

def temp_gesd(data_escolhida, coluna_escolhida):
    df = pd.read_csv('DUSTAINEW.csv', sep=';', decimal=',')
    df['Datetime'] = pd.to_datetime(df['Datetime'])  

    df = df[df['Datetime'].dt.date == data_escolhida]
    
    temperatura_column = df[coluna_escolhida]  
    horas = df['Datetime']
    horas = horas.dt.strftime('%H:%M')
    
    min_datetime = min(df['Datetime'])
    max_datetime = max(df['Datetime'])
    
    outliers_indices = sp.outliers_gesd(temperatura_column, outliers=5, alpha=0.05)
    gesd = df.iloc[outliers_indices]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=45))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set(xlabel='Horas', ylabel=coluna_escolhida, title=f'{coluna_escolhida} GESD', xlim=[min_datetime, max_datetime])
    ax.plot(df['Datetime'], temperatura_column, label=coluna_escolhida, linewidth=2, color='blue')
    ax.scatter(list(gesd['Datetime']), list(gesd[coluna_escolhida]), color='red', label='Outliers', zorder=5)
    ax.grid(True)
    fig.autofmt_xdate()
    plt.show()

if __name__ == '__main__':
    while True:
        print('Escolha a coluna a ser analisada:')
        print('(1) Temperatura')
        print('(2) Umidade')
        print('(3) MP2,5_1')
        print('(4) MP10_1')
        print('(5) MP2,5_2')
        print('(6) MP10_2')
        print('(7) Sair')
        opcao_coluna = int(input('Digite a opção desejada: '))
        if opcao_coluna == 1:
            coluna_escolhida = 'Temperatura'
        elif opcao_coluna == 2:
            coluna_escolhida = 'Umidade'
        elif opcao_coluna == 3:
            coluna_escolhida = 'MP2,5_1'
        elif opcao_coluna == 4:
            coluna_escolhida = 'MP10_1'
        elif opcao_coluna == 5:
            coluna_escolhida = 'MP2,5_2'
        elif opcao_coluna == 6:
            coluna_escolhida = 'MP10_2'
        elif opcao_coluna == 7:
            break
        else:
            print('Opção inválida!')
            continue
        
        
        
        print('Escolha uma das opções abaixo:')
        print('(1) Geral')
        print('(2) Outliers')
        print('(3) Picos de Erros')
        print('(4) Valores Stuck')
        print('(5) Variância')
        print('(6) Outliers 3 sigma')
        print('(7) GESD')
        print('(8) Sair')
        opcao = int(input('Digite a opção desejada: '))
        if opcao == 1:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            temp_geral(pd.to_datetime(data_escolhida, dayfirst=True).date(),coluna_escolhida)
        elif opcao == 2:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            temp_outliers(pd.to_datetime(data_escolhida, dayfirst=True).date(),coluna_escolhida)
        elif opcao == 3:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            temp_peak(pd.to_datetime(data_escolhida, dayfirst=True).date(),coluna_escolhida)
        elif opcao == 4:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            resultados = temp_stuck(pd.to_datetime(data_escolhida, dayfirst=True).date(),coluna_escolhida)
            print(resultados)
                
        elif opcao == 5:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            resultados = temp_variance(pd.to_datetime(data_escolhida, dayfirst=True).date(),coluna_escolhida)
            # print(resultados)
        elif opcao == 6:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            temp_outlier_3sigma(pd.to_datetime(data_escolhida, dayfirst=True).date(),coluna_escolhida)    
        elif opcao == 7:
            data_escolhida = input('Digite a data no formato dd/mm/aaaa: ')
            temp_gesd(pd.to_datetime(data_escolhida, dayfirst=True).date(),coluna_escolhida)    
        elif opcao == 8:
            break
        else:
            print('Opção inválida!')
    