import pandas as pd

# Lê o arquivo CSV
df = pd.read_csv('DUSTAINEW.csv', sep=';')

# Converte a coluna 'HoraNew' para o tipo datetime
df_hora = pd.to_datetime(df['HoraNew'], format='%H:%M:%S').dt.time  # Especificar o formato
df['DataNew'] = pd.to_datetime(df['DataNew'],dayfirst=True)
# Verifica o novo tipo de dados da coluna 'HoraNew'
tipo_dados_hora_new = df['HoraNew'].dtype
tipo_dados_date_new = df['DataNew'].dtype

# print("Novo tipo de dados da coluna 'HoraNew':", tipo_dados_hora_new)
# print("Novo tipo de dados da coluna 'DataNew':", tipo_dados_date_new)
print(df_hora)