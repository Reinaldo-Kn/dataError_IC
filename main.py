import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def temp_geral():
    df = pd.read_csv('DUSTAI.csv', sep=';', decimal=',')
    
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, infer_datetime_format=True)
    df = df.set_index('Data')
    
    max_temperaturas = df.groupby(df.index.date)['Temperatura'].max()
    plt.figure(figsize=(10, 6))
    plt.scatter(max_temperaturas.index, max_temperaturas.values, color='red', label='Maior Valor', s=100, alpha=1)
    plt.plot(max_temperaturas.index, max_temperaturas.values, color='red', alpha=0.5)
    plt.title('Temperatura')
    plt.xlabel('Data')
    plt.ylabel('Temperatura')
    plt.legend()
    plt.show()


def temp_outliers():
    df = pd.read_csv('DUSTAI.csv', sep = ';', decimal = ',')
    df['Data'] = pd.to_datetime(df['Data'], dayfirst = True, infer_datetime_format = True)
    df = df.set_index('Data')

    temperatura_column = df['Temperatura']
    Q1 = temperatura_column.quantile(0.25)
    Q3 = temperatura_column.quantile(0.75)
    IQR = Q3 - Q1

    threshold = 0.75
    lower_limit = Q1 - threshold * IQR
    upper_limit = Q3 + threshold * IQR

    outliers = temperatura_column[(temperatura_column < lower_limit) | (temperatura_column > upper_limit)]

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, temperatura_column, label='Temperatura')
    plt.scatter(outliers.index, outliers, color='red', label=f'Outliers com threshold: {threshold}')
    plt.title('Temperatura com Outliers')
    plt.xlabel('Data')
    plt.ylabel('Temperatura')
    plt.legend()
    plt.show()

    print(IQR)
    print(Q1)
    print(Q3)
    print(df['Temperatura'].describe())
        
        
def temp_peak():
    df = pd.read_csv('DUSTAI.csv', sep=';', decimal=',')
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, infer_datetime_format=True)
    df = df.set_index('Data')
    temperatura_column = df['Temperatura']
    
    mean_temp = temperatura_column.mean()
    std_temp = temperatura_column.std()
    spike_threshold = 1.75

    spike_errors = temperatura_column[abs(temperatura_column - mean_temp) > spike_threshold * std_temp]
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, temperatura_column, label='Temperatura')
    plt.scatter(spike_errors.index, spike_errors, color='red', label='Picos de Erros')
    plt.axhline(y=mean_temp, color='green', linestyle='--', label=f'Média: {mean_temp:.2f}')
    plt.axhline(y=mean_temp + spike_threshold * std_temp, color='orange', linestyle='--', label=f' Desvios padrão: {spike_threshold}')
    plt.axhline(y=mean_temp - spike_threshold * std_temp, color='orange', linestyle='--')
    plt.title('Temperatura com Picos de Erros')
    plt.xlabel('Data')
    plt.ylabel('Temperatura')
    plt.legend()
    plt.show()
    

def temp_stuck():
    df = pd.read_csv('DUSTAI.csv', sep=';', decimal=',')
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, infer_datetime_format=True)
    df = df.set_index('Data')
    
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

def temp_variance():
    df = pd.read_csv('DUSTAI.csv', sep=';', decimal=',')
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, infer_datetime_format=True)
    df = df.set_index('Data')  
    temperaturas = df['Temperatura']
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
            temp_geral()
        elif opcao == 2:
            temp_outliers()
        elif opcao == 3:
            temp_peak()
        elif opcao == 4:
            resultados = temp_stuck()
            print(resultados)
                
        elif opcao == 5:
            resultados = temp_variance()
            print(resultados)
            
        elif opcao == 6:
            break
        else:
            print('Opção inválida!')
    