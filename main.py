import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, confusion_matrix

# 1. Load Data
file_path = "traffic_small.csv"

try:
    df = pd.read_csv(file_path)
    print("Loaded dataset")
except:
    print("File not found")
    sys.exit()

speed_col = 'SpaceMeanSpeed'
flow_col = 'TrafficFlow'

# 2. Clean Data
df = df[(df[speed_col] > 0) & (df[flow_col] > 0)]
df = df.dropna()

# 3. Ground Truth
df['Actual_Density'] = df[flow_col] / df[speed_col]

# 4. Greenshields Model
vf = df[speed_col].quantile(0.95)
kj = df['Actual_Density'].quantile(0.95)

df['Greenshields_Density'] = kj * (1 - (df[speed_col] / vf))
df['Greenshields_Density'] = df['Greenshields_Density'].clip(lower=0)

# 5. FUZZY SYSTEM

df['speed_norm'] = df[speed_col] / df[speed_col].max()
df['flow_norm'] = df[flow_col] / df[flow_col].max()

speed = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'speed')
flow = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'flow')
density = ctrl.Consequent(np.arange(0, df['Actual_Density'].max()+1, 1), 'density')

speed['low'] = fuzz.gaussmf(speed.universe, 0.2, 0.15)
speed['medium'] = fuzz.gaussmf(speed.universe, 0.5, 0.15)
speed['high'] = fuzz.gaussmf(speed.universe, 0.8, 0.15)

flow['low'] = fuzz.gaussmf(flow.universe, 0.2, 0.15)
flow['medium'] = fuzz.gaussmf(flow.universe, 0.5, 0.15)
flow['high'] = fuzz.gaussmf(flow.universe, 0.8, 0.15)

d_max = df['Actual_Density'].max()

density['low'] = fuzz.gaussmf(density.universe, d_max*0.2, d_max*0.1)
density['medium'] = fuzz.gaussmf(density.universe, d_max*0.5, d_max*0.1)
density['high'] = fuzz.gaussmf(density.universe, d_max*0.8, d_max*0.1)

rules = [
    ctrl.Rule(speed['high'] & flow['low'], density['low']),
    ctrl.Rule(speed['high'] & flow['medium'], density['low']),
    ctrl.Rule(speed['high'] & flow['high'], density['medium']),
    ctrl.Rule(speed['medium'] & flow['low'], density['low']),
    ctrl.Rule(speed['medium'] & flow['medium'], density['medium']),
    ctrl.Rule(speed['medium'] & flow['high'], density['high']),
    ctrl.Rule(speed['low'] & flow['low'], density['medium']),
    ctrl.Rule(speed['low'] & flow['medium'], density['high']),
    ctrl.Rule(speed['low'] & flow['high'], density['high']),
]

traffic_ctrl = ctrl.ControlSystem(rules)

# Ratio normalization bounds
ratio_series = df[flow_col] / df[speed_col]
ratio_min = ratio_series.min()
ratio_max = ratio_series.max()

# Label thresholds
low_thresh = d_max * 0.33
high_thresh = d_max * 0.66

def get_label(value):
    if value <= low_thresh:
        return "Low"
    elif value <= high_thresh:
        return "Medium"
    else:
        return "High"

# Prediction function
def predict_density(speed_input, flow_input):
    traffic_sim = ctrl.ControlSystemSimulation(traffic_ctrl)

    speed_norm = speed_input / df[speed_col].max()
    flow_norm = flow_input / df[flow_col].max()

    try:
        traffic_sim.input['speed'] = speed_norm
        traffic_sim.input['flow'] = flow_norm
        traffic_sim.compute()
        fuzzy_density = traffic_sim.output['density']
    except:
        fuzzy_density = 0

    greenshields_density = kj * (1 - (speed_input / vf))
    greenshields_density = max(0, greenshields_density)

    ratio = flow_input / speed_input
    if ratio_max != ratio_min:
        ratio_norm = (ratio - ratio_min) / (ratio_max - ratio_min)
    else:
        ratio_norm = 0.5

    hybrid_density = (
        ratio_norm * fuzzy_density +
        (1 - ratio_norm) * greenshields_density
    )

    label = get_label(hybrid_density)

    return hybrid_density, label

# Generate predictions
hybrid_results = []
labels = []

for i in range(len(df)):
    density, label = predict_density(df[speed_col].iloc[i], df[flow_col].iloc[i])
    hybrid_results.append(density)
    labels.append(label)

df['Hybrid_Density'] = hybrid_results
df['Hybrid_Label'] = labels
df['Actual_Label'] = df['Actual_Density'].apply(get_label)

# Regression evaluation
def evaluate(true, pred, name):
    rmse = np.sqrt(mean_squared_error(true, pred))
    mae = mean_absolute_error(true, pred)
    r2 = r2_score(true, pred)
    print(f"\n{name}:")
    print(f"RMSE: {rmse:.3f}")
    print(f"MAE: {mae:.3f}")
    print(f"R2: {r2:.3f}")

print("\nMODEL COMPARISON")
evaluate(df['Actual_Density'], df['Greenshields_Density'], "Greenshields")
evaluate(df['Actual_Density'], df['Hybrid_Density'], "Hybrid")

# Classification metrics
accuracy = accuracy_score(df['Actual_Label'], df['Hybrid_Label'])
error_rate = 1 - accuracy

print("\nCLASSIFICATION METRICS")
print(f"Accuracy: {accuracy:.3f}")
print(f"Error Rate: {error_rate:.3f}")

cm = confusion_matrix(df['Actual_Label'], df['Hybrid_Label'], labels=["Low", "Medium", "High"])
print("\nConfusion Matrix:")
print(cm)

# Sample output
print("\nSample Predictions:\n")
sample_df = df[[speed_col, flow_col, 'Actual_Density', 'Hybrid_Density', 'Hybrid_Label']].head(10)
print(sample_df.round(2).to_string(index=False))

# Visualization
plt.figure()
plt.scatter(df[speed_col], df['Actual_Density'], label='Actual', alpha=0.6)
plt.scatter(df[speed_col], df['Greenshields_Density'], label='Greenshields', alpha=0.6)
plt.scatter(df[speed_col], df['Hybrid_Density'], label='Hybrid', alpha=0.6)

plt.xlabel("Speed")
plt.ylabel("Density")
plt.legend()
plt.title("Hybrid vs Greenshields")
plt.show()

# User input mode
print("\n--- Traffic Prediction System ---")

while True:
    try:
        speed_in = float(input("\nEnter Speed (or -1 to exit): "))
        if speed_in == -1:
            break

        flow_in = float(input("Enter Traffic Flow: "))

        density, label = predict_density(speed_in, flow_in)

        print(f"\nPredicted Density: {density:.2f}")
        print(f"Traffic Level: {label}")

    except:
        print("Invalid input. Try again.")