import pandas as pd

# Lê o arquivo CSV
df = pd.read_csv('DUSTAI.csv', sep=';')

# Converte as colunas 'Hora' e 'Data' para os formatos desejados
df['HoraNew'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.strftime('%H:%M:%S')
df['DataNew'] = pd.to_datetime(df['Data'], format='%d/%m/%y').dt.strftime('%d/%m/%Y')

# Cria a nova coluna 'Datetime' concatenando as colunas 'DataNew' e 'HoraNew'
df['Datetime'] = pd.to_datetime(df['DataNew'] + ' ' + df['HoraNew'], format='%d/%m/%Y %H:%M:%S')

# Salva o DataFrame atualizado em um novo arquivo CSV
df.to_csv('DUSTAINEW.csv', index=False, sep=';', decimal=',')

print("Novo arquivo 'DUSTAINEW.csv' criado com sucesso!")
