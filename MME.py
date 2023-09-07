import MetaTrader5 as mt
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib import style

input_data = yf.download('MSFT', '2020-01-01', '2020-01-20').reset_index()
#print(input_data)

#media movel simple
window = 14
input_data['SMA'] = input_data['Adj Close'].rolling(window).mean()
#print(input_data)

#media movel exponencial
window = 10
input_data[f'EMA{window}'] = input_data['Adj Close'].ewm(span=window).mean()
#print(input_data)

#R S I
import pandas as pd
df = input_data.copy()
#calcural a variação
df['change'] = df['Close'] - df['Close'].shift(1)
# separar/indentificar entre periodos de ganhos e perda
df['gain'] = df.loc[df['change']>0, 'change'].apply(abs)
df.loc[(df['gain'].isna()), 'gain'] = 0
df.loc[0, 'gain'] = np.NAN

df['loss'] = df.loc[df['change']>0, 'change'].apply(abs)
df.loc[(df['loss'].isna()), 'loss'] = 0
df.loc[0, 'loss'] = np.NAN

#calcular media movel (ganhos e perdas)
window = 14
df['avg_gain'] = df['gain'].rolling(window).mean()
df['avg_loss'] = df['loss'].rolling(window).mean()

first = df['avg_gain'].first_valid_index()
print(first)
for index, row in df.iterrows():
    if index == first:
        prev_avg_gain = row['avg_gain']
        prev_avg_loss = row['avg_loss']

    elif index > first:
        df.loc[index, 'avg_gain'] = ((prev_avg_gain * (window - 1)) + row['gain'])/window
        prev_avg_gain = df.loc[index, 'avg_gain']

        df.loc[index, 'avg_loss'] = ((prev_avg_loss * (window - 1)) + row['loss']) / window
        prev_avg_loss = df.loc[index, 'avg_loss']
    #calcular RS
    df[f'RS{window}'] = df['avg_gain']/df['avg_loss']
    #calcula RSI
    df[f'RSI{window}'] = 100 - (100/(1 + df[f'RS{window}']))
    print(df)