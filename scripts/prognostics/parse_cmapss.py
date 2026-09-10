import os
import urllib.request
import pandas as pd

for f in ['train_FD001.txt', 'test_FD001.txt', 'RUL_FD001.txt']:
    if os.path.exists(f): 
        os.remove(f)

# Using a confirmed, stable mirror for the CMAPSS dataset
base_url = "https://raw.githubusercontent.com/hankroark/Turbofan-Engine-Degradation/master/CMAPSSData/"
urllib.request.urlretrieve(base_url + 'train_FD001.txt', 'train_FD001.txt')
urllib.request.urlretrieve(base_url + 'test_FD001.txt', 'test_FD001.txt')
urllib.request.urlretrieve(base_url + 'RUL_FD001.txt', 'RUL_FD001.txt')

col_names = ['unit', 'cycle', 'op1', 'op2', 'op3'] + [f'sensor_{i}' for i in range(1, 22)]
train_df = pd.read_csv('train_FD001.txt', sep=r'\s+', header=None, names=col_names)
test_df = pd.read_csv('test_FD001.txt', sep=r'\s+', header=None, names=col_names)
rul_true = pd.read_csv('RUL_FD001.txt', sep=r'\s+', header=None, names=['rul'])

train_df['unit'] = pd.to_numeric(train_df['unit'])
train_df['cycle'] = pd.to_numeric(train_df['cycle'])

max_cycles = train_df.groupby('unit')['cycle'].max().reset_index()
max_cycles.columns = ['unit', 'max_cycle']
train_df = train_df.merge(max_cycles, on='unit', how='left')
train_df['RUL'] = train_df['max_cycle'] - train_df['cycle']
train_df.drop('max_cycle', axis=1, inplace=True)

print(f"Train shape: {train_df.shape}")
print(f"Test shape: {test_df.shape}")
print(f"True RUL shape: {rul_true.shape}")
print(train_df[['unit', 'cycle', 'sensor_2', 'sensor_3', 'sensor_4', 'RUL']].head())
