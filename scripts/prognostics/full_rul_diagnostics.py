import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')  # Headless backend to prevent X server errors in Termux
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore')

print("\n[*] INITIALIZING ADVANCED THREE-LINEAGE RUL ENGINE...")

# Load Datasets
col_names = ['unit', 'cycle', 'op1', 'op2', 'op3'] + [f'sensor_{i}' for i in range(1, 22)]
train_df = pd.read_csv('data/cmapss/train_FD001.txt', sep=r'\s+', header=None, names=col_names)
test_df = pd.read_csv('data/cmapss/test_FD001.txt', sep=r'\s+', header=None, names=col_names)
rul_true = pd.read_csv('data/cmapss/RUL_FD001.txt', sep=r'\s+', header=None, names=['rul'])

train_df['unit'] = pd.to_numeric(train_df['unit'])
train_df['cycle'] = pd.to_numeric(train_df['cycle'])

# Calculate Ground Truth RUL for Training
max_cycles = train_df.groupby('unit')['cycle'].max().reset_index()
max_cycles.columns = ['unit', 'max_cycle']
train_df = train_df.merge(max_cycles, on='unit', how='left')
train_df['RUL'] = train_df['max_cycle'] - train_df['cycle']
train_df.drop('max_cycle', axis=1, inplace=True)

# --- [1] MULTI-UNIT CORRELATION ANALYSIS ---
print("\n--- [1] MULTI-UNIT CORRELATION ANALYSIS ---")
active_cols = train_df.columns[train_df.std() > 0.01].drop(['unit', 'cycle', 'op1', 'op2', 'op3', 'RUL'], errors='ignore')
global_corr = train_df[active_cols.tolist() + ['RUL']].corr()['RUL'].drop('RUL')
top_features = global_corr.abs().sort_values(ascending=False).head(5).index.tolist()
print(f"Top 5 Globally Correlated Degradation Sensors: {top_features}")
print(global_corr[top_features].to_string())

# --- [2] DEEPER DRIFT MODELLING ---
print("\n--- [2] DEEP DRIFT MODELLING (SMOOTHED) ---")
# Apply a rolling window to smooth noise and extract the pure degradation signal
primary_sensor = top_features[0]
train_df['drift_signal'] = train_df.groupby('unit')[primary_sensor].transform(lambda x: x.rolling(window=10, min_periods=1).mean())
print(f"Computed 10-cycle rolling average drift for {primary_sensor} across all units.")

# --- [3] PLOT DEGRADATION CURVES ---
print("\n--- [3] PLOTTING DEGRADATION CURVES ---")
plt.figure(figsize=(10, 6))
for unit in range(1, 6):  # Plot first 5 units
    unit_data = train_df[train_df['unit'] == unit]
    plt.plot(unit_data['cycle'], unit_data['drift_signal'], label=f'Unit {unit}')

plt.title(f'Degradation Curves ({primary_sensor}) - Signal Drift Over Time')
plt.xlabel('Operational Cycles')
plt.ylabel(f'Smoothed {primary_sensor} Output')
plt.legend()
plt.grid(True)
plot_path = 'degradation_curves.png'
plt.savefig(plot_path)
print(f"[+] Degradation plot saved successfully to: {plot_path}")

# --- [4] FULL MULTIVARIATE RUL MODEL ---
print("\n--- [4] BUILDING RUL PREDICTION MODEL ---")
# Using purely NumPy-based Multiple Linear Regression to avoid heavy scikit-learn compilation in Termux
X_train = train_df[top_features].values
X_train = np.c_[np.ones(X_train.shape[0]), X_train]  # Add bias column
y_train = train_df['RUL'].values

# Normal Equation: theta = (X^T * X)^-1 * X^T * y
theta = np.linalg.inv(X_train.T.dot(X_train)).dot(X_train.T).dot(y_train)
print("[+] Model trained successfully using Normal Equation.")
print(f"Model Weights (Theta): {np.round(theta, 3)}")

# --- [5] REPLAY ENGINE ACROSS ALL UNITS (TEST SET) ---
print("\n--- [5] REPLAY ENGINE: MULTI-UNIT SIMULATION ---")
# Prepare test data ground truth
test_max_cycles = test_df.groupby('unit')['cycle'].max().reset_index()
print("[*] Replaying operational streams for Test Units 1-3 (Truncated for terminal output)...")

intercept_threshold = 30  # Trigger governance intercept when predicted RUL falls below 30 cycles

for unit_id in range(1, 4):  # Replay first 3 test units
    unit_stream = test_df[test_df['unit'] == unit_id]
    true_rul_final = rul_true.iloc[unit_id - 1].values[0]
    final_cycle = test_max_cycles[test_max_cycles['unit'] == unit_id]['cycle'].values[0]
    
    print(f"\n[>] Initiating stream for Unit {unit_id} (Total recorded test cycles: {final_cycle})")
    intercepted = False
    
    for _, row in unit_stream.iterrows():
        cycle = int(row['cycle'])
        features = row[top_features].values
        x_in = np.insert(features, 0, 1)
        pred_rul = x_in.dot(theta)
        
        # Calculate approximate true RUL at this specific cycle
        current_true_rul = true_rul_final + (final_cycle - cycle)

        if pred_rul <= intercept_threshold:
            print(f"    [!] GOVERNANCE INTERCEPT: Predicted RUL fell to {pred_rul:.1f} cycles.")
            print(f"        Intercepted at Cycle {cycle}. Actual remaining cycles: {current_true_rul}")
            intercepted = True
            break
            
    if not intercepted:
        print(f"    [*] Unit {unit_id} completed stream without breaching critical RUL threshold.")
        print(f"        Final Predicted RUL: {pred_rul:.1f} | Actual Final RUL: {true_rul_final}")

print("\n[*] FULL ARCHITECTURE EXECUTION COMPLETE.")
