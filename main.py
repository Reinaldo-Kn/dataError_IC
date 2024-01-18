import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def temp_geral():
    df = pd.read_csv('DUSTAI.csv', sep=';', decimal=',')
    
    # Converte a coluna 'Data' para o formato datetime e a define como índice
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, infer_datetime_format=True)
    df = df.set_index('Data')
    
    max_temperaturas = df.groupby(df.index.date)['Temperatura'].max()
    plt.figure(figsize=(10, 6))
    plt.scatter(max_temperaturas.index, max_temperaturas.values, color='red', label='Maior Valor', s=100, alpha=1)
    plt.plot(max_temperaturas.index, max_temperaturas.values, color='red', alpha=0.5)
    plt.title('Temperatura')
    plt.xlabel('Data')
    plt.ylabel('Temperatura')
    
    # Adiciona legenda
    plt.legend()
    
    # Exibe o gráfico
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

    # Calcular a média e o desvio padrão da temperatura
    mean_temp = temperatura_column.mean()
    std_temp = temperatura_column.std()

    # Definir um limite para identificar picos de erros (por exemplo, 3 desvios padrão)
    spike_threshold = 1.75

    # Identificar picos de erros
    spike_errors = temperatura_column[abs(temperatura_column - mean_temp) > spike_threshold * std_temp]

    # Plotar o gráfico de temperatura com picos de erros destacados
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
    # Leitura do arquivo CSV
    df = pd.read_csv('DUSTAI.csv', sep=';', decimal=',')
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, infer_datetime_format=True)
    df = df.set_index('Data')

    # Inicializando vetor para armazenar resultados
    resultados = []

    # Parâmetros
    tamanho_sequencia = 30
    threshold_variancia = 0.25

    # Iterando sobre as temperaturas
    for i in range(len(df) - tamanho_sequencia + 1):
        sequencia = df['Temperatura'].iloc[i:i+tamanho_sequencia]
        media_sequencia = round(sequencia.mean(), 2)
        variancia_sequencia = round(sequencia.var(), 2)

        if variancia_sequencia <= threshold_variancia:
            # Verifica se todos os valores estão dentro do intervalo [média - threshold, média + threshold]
            if all(media_sequencia - threshold_variancia <= valor <= media_sequencia + threshold_variancia for valor in sequencia):
                id_correspondente = df['Num'].iloc[i]
                resultados.append((id_correspondente, media_sequencia))

    return resultados
    


if __name__ == '__main__':
    while True:
        print('Escolha uma das opções abaixo:')
        print('1. Temperatura Geral')
        print('2. Temperatura com Outliers')
        print('3. Temperatura com Picos de Erros')
        print('4. Temperatura com Valores Fixos')
        print('5. Sair')
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
            break
        else:
            print('Opção inválida!')
    