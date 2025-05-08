# Step 1: Import necessary libraries
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.graph_objects as go

# Step 2: Load your data from the CSV file
# Replace 'dht11_data.csv' with the actual filename of your data file
try:
    df = pd.read_csv('dht11_data.csv')
except FileNotFoundError:
    print("Error: CSV file not found. Please make sure 'dht11_data.csv' is in the correct directory.")
    exit()

# Assuming your CSV has columns named 'Temperature' and 'Humidity'
# If your column names are different, replace them accordingly
try:
    X = df[['Temperature']]  # Independent variable (temperature)
    y = df['Humidity']      # Dependent variable (humidity)
except KeyError:
    print("Error: Ensure your CSV file has columns named 'Temperature' and 'Humidity'.")
    exit()

# --- Scenario 1: Linear Regression on the original dataset ---
model_original = LinearRegression()
model_original.fit(X, y)
min_temp_original = df['Temperature'].min()
max_temp_original = df['Temperature'].max()
test_temp_original = np.linspace(min_temp_original, max_temp_original, 100).reshape(-1, 1)
predicted_humidity_original = model_original.predict(test_temp_original)

# --- Scenario 2: Linear Regression after the first filtering of potential outliers ---
min_temp_threshold_1 = 15  # Adjust these based on your data
max_temp_threshold_1 = 35
df_filtered_1 = df[(df['Temperature'] >= min_temp_threshold_1) & (df['Temperature'] <= max_temp_threshold_1)].copy()
X_filtered_1 = df_filtered_1[['Temperature']]
y_filtered_1 = df_filtered_1['Humidity']
model_filtered_1 = LinearRegression()
model_filtered_1.fit(X_filtered_1, y_filtered_1)
min_temp_filtered_1 = df_filtered_1['Temperature'].min()
max_temp_filtered_1 = df_filtered_1['Temperature'].max()
test_temp_filtered_1 = np.linspace(min_temp_filtered_1, max_temp_filtered_1, 100).reshape(-1, 1)
predicted_humidity_filtered_1 = model_filtered_1.predict(test_temp_filtered_1)

# --- Scenario 3: Linear Regression after the second filtering of potential outliers ---
min_temp_threshold_2 = 18  # Adjust these based on your data
max_temp_threshold_2 = 32
df_filtered_2 = df[(df['Temperature'] >= min_temp_threshold_2) & (df['Temperature'] <= max_temp_threshold_2)].copy()
X_filtered_2 = df_filtered_2[['Temperature']]
y_filtered_2 = df_filtered_2['Humidity']
model_filtered_2 = LinearRegression()
model_filtered_2.fit(X_filtered_2, y_filtered_2)
min_temp_filtered_2 = df_filtered_2['Temperature'].min()
max_temp_filtered_2 = df_filtered_2['Temperature'].max()
test_temp_filtered_2 = np.linspace(min_temp_filtered_2, max_temp_filtered_2, 100).reshape(-1, 1)
predicted_humidity_filtered_2 = model_filtered_2.predict(test_temp_filtered_2)

# --- Create a single plot with all scenarios ---
fig = go.Figure()

# Add scatter plot for original data
fig.add_trace(go.Scatter(x=df['Temperature'], y=df['Humidity'], mode='markers', name='Original Data'))

# Add line plot for the trend line of original data
fig.add_trace(go.Scatter(x=test_temp_original.flatten(), y=predicted_humidity_original, mode='lines', name='Trend Line (Original)', line=dict(color='red')))

# Add scatter plot for the first filtered data
fig.add_trace(go.Scatter(x=df_filtered_1['Temperature'], y=df_filtered_1['Humidity'], mode='markers', name='Filtered Data 1'))

# Add line plot for the trend line of the first filtered data
fig.add_trace(go.Scatter(x=test_temp_filtered_1.flatten(), y=predicted_humidity_filtered_1, mode='lines', name='Trend Line (Filtered 1)', line=dict(color='green')))

# Add scatter plot for the second filtered data
fig.add_trace(go.Scatter(x=df_filtered_2['Temperature'], y=df_filtered_2['Humidity'], mode='markers', name='Filtered Data 2'))

# Add line plot for the trend line of the second filtered data
fig.add_trace(go.Scatter(x=test_temp_filtered_2.flatten(), y=predicted_humidity_filtered_2, mode='lines', name='Trend Line (Filtered 2)', line=dict(color='purple')))

# Set the title and axis labels
fig.update_layout(title='Temperature vs Humidity with Linear Regression Trends (All Scenarios)',
                  xaxis_title='Temperature (°C)',
                  yaxis_title='Humidity (%)')

# Show the plot
fig.show()