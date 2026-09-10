import pandas as pd
import numpy as np

# Suppress pandas FutureWarnings for clean output
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# 1. Load Data
col_names = ['unit', 'cycle', 'op1', 'op2', 'op3'] + [f'sensor_{i}' for i in range(1, 22)]
df = pd.read_csv('train_FD001.txt', sep=r'\s+', header=None, names=col_names)
df['unit'] = pd.to_numeric(df['unit'])
df['cycle'] = pd.to_numeric(df['cycle'])

# RUL Calculation
max_cycles = df.groupby('unit')['cycle'].max().reset_index()
max_cycles.columns = ['unit', 'max_cycle']
df = df.merge(max_cycles, on='unit', how='left')
df['RUL'] = df['max_cycle'] - df['cycle']

print("\n[*] INITIALIZING THREE-LINEAGE RUL DIAGNOSTICS...")

# [1] UNIT-LEVEL DEGRADATION PROFILING
print("\n--- [1] UNIT-LEVEL DEGRADATION PROFILING ---")
print("Baseline lifespan variance across first 3 operational units:")
print(df.groupby('unit')['cycle'].max().head(3).to_string())

# [2] SENSOR CORRELATION MAPPING
print("\n--- [2] SENSOR CORRELATION MAPPING ---")
# Drop constant sensors (standard deviation near zero)
active_cols = df.columns[df.std() > 0.01]
df_active = df[active_cols]
# Map correlations against the RUL vector
corr = df_active.corr()['RUL'].drop(['unit', 'cycle', 'RUL', 'max_cycle'], errors='ignore')
top_pos = corr.idxmax() # Decreases as RUL decreases
top_neg = corr.idxmin() # Increases as RUL decreases
print(f"Primary Positive Drift Indicator: {top_pos} (Corr: {corr[top_pos]:.3f})")
print(f"Primary Negative Drift Indicator: {top_neg} (Corr: {corr[top_neg]:.3f})")

# [3] SIGNAL DRIFT ANALYSIS
print("\n--- [3] SIGNAL DRIFT ANALYSIS (UNIT 1) ---")
u1 = df[df['unit'] == 1]
baseline_val = u1[top_neg].head(10).mean()
critical_val = u1[top_neg].tail(10).mean()
drift = critical_val - baseline_val
print(f"Tracking {top_neg}: Baseline {baseline_val:.2f} -> Critical {critical_val:.2f} (Total Drift: {drift:.2f})")

# [4 & 5] RUL MODELLING & REPLAY ENGINE TESTING
print("\n--- [4 & 5] RUL MODELLING & REPLAY ENGINE TESTING ---")
# Set an early-warning governance intercept at 70% of known terminal degradation
threshold = baseline_val + (drift * 0.70)
print(f"Governance Ceiling (Intercept Threshold) set at: {threshold:.2f}\n")

print("[*] Commencing stream replay for Unit 1...")
intercepted = False
for _, row in u1.iterrows():
    cycle = int(row['cycle'])
    val = row[top_neg]
    
    # Trigger intercept if sensor breaches the degradation threshold
    if (drift > 0 and val >= threshold) or (drift < 0 and val <= threshold):
        print(f"[!] GOVERNANCE CEILING BREACH: Critical degradation signature detected.")
        print(f"    Action: captured_disarmed_learned_and_traced")
        print(f"    Intercepted at Cycle {cycle} | Sensor Value: {val:.2f}")
        print(f"    True RUL remaining at intercept: {int(row['RUL'])} cycles before total failure.")
        intercepted = True
        break

if not intercepted:
    print("[*] Unit operated within governance limits.")
print("\n[*] DIAGNOSTICS COMPLETE.")
