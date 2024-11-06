"""TRATAMENTO DA BASE DE DADOS"""

import pandas as pd


df = pd.read_csv('base/Crime_Data_from_2020_to_Present.csv')

df = df.drop(['Crm Cd', 'Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4',
              'Cross Street', 'LOCATION', 'Mocodes', 'Premis Cd',
              'AREA', 'Rpt Dist No', 'Part 1-2', 'Weapon Used Cd'],
             axis=1)

# Removendo valores de Sexo da Vítima que não são válidos
indexes_to_drop = df[df['Vict Sex'].isin(values=['H', '-'])].index
df = df.drop(indexes_to_drop)

# Transformando a coluna DATE OCC para datetime
df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], errors='coerce')

# Criando coluna YearMonth, apenas com valores de Mês e Ano
df['YearMonth'] = df['DATE OCC'].dt.to_period('M').astype(str)

# Removendo valores de Idade da Vítima que são menores ou iguais a 0
df['Vict Age'] = pd.to_numeric(df['Vict Age'], errors='coerce')
df = df[(df['Vict Age'] > 0) & (df['Vict Age'] < 110)]

# Função para classificar os horários
def classificar_periodo(time):
    if 1 <= time <= 500:
        return 'Madrugada'
    elif 501 <= time <= 1200:
        return 'Manhã'
    elif 1201 <= time <= 1800:
        return 'Tarde'
    elif 1801 <= time <= 2359:
        return 'Noite'
    else:
        return 'Desconhecido'

# Aplicando a função a cada valor da coluna 'Time'
df['Periodo'] = df['TIME OCC'].apply(classificar_periodo)

# Salvando o DF
df.to_csv('base/Crime_Data_Treated.csv', index=False)


