import pandas as pd

df = pd.read_csv('DUSTAI.csv', sep=';')

df['HoraNew'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.strftime('%H:%M:%S')
df['DataNew'] = pd.to_datetime(df['Data'], format='%d/%m/%y').dt.strftime('%d/%m/%Y')

df['Datetime'] = pd.to_datetime(df['DataNew'] + ' ' + df['HoraNew'], format='%d/%m/%Y %H:%M:%S')

df.to_csv('DUSTAINEW.csv', index=False, sep=';', decimal=',')

print("Novo arquivo 'DUSTAINEW.csv' criado com sucesso!")
