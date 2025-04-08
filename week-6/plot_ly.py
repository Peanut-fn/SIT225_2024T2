import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load dataset
df = pd.read_csv("gyro_data.csv")

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Gyroscope Data Dashboard"),
    
    # Dropdown for selecting graph type
    html.Label("Select Graph Type:"),
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Distribution Plot', 'value': 'hist'}
        ],
        value='line'
    ),

    # Dropdown for selecting gyroscope axis
    html.Label("Select Axis:"),
    dcc.Dropdown(
        id='axis',
        options=[
            {'label': 'X', 'value': 'gyro_x'},
            {'label': 'Y', 'value': 'gyro_y'},
            {'label': 'Z', 'value': 'gyro_z'},
            {'label': 'All', 'value': 'all'}
        ],
        value='all'
    ),

    # Input box for number of samples
    html.Label("Number of Samples:"),
    dcc.Input(id='num-samples', type='number', value=100, min=1),

    # Next/Previous Buttons
    html.Button("Previous", id="prev-btn", n_clicks=0),
    html.Button("Next", id="next-btn", n_clicks=0),

    # Graph
    dcc.Graph(id='gyro-graph'),

    # Data summary table
    html.H2("Data Summary"),
    html.Div(id='data-summary')
])

# Callback to update the graph
@app.callback(
    Output('gyro-graph', 'figure'),
    Output('data-summary', 'children'),
    Input('graph-type', 'value'),
    Input('axis', 'value'),
    Input('num-samples', 'value'),
    Input('prev-btn', 'n_clicks'),
    Input('next-btn', 'n_clicks')
)
def update_graph(graph_type, axis, num_samples, prev_clicks, next_clicks):
    start_idx = (prev_clicks - next_clicks) * num_samples
    data_subset = df.iloc[start_idx:start_idx + num_samples]

    if axis == "all":
        fig = px.line(data_subset, x='timestamp', y=['gyro_x', 'gyro_y', 'gyro_z']) if graph_type == "line" else \
              px.scatter(data_subset, x='timestamp', y=['gyro_x', 'gyro_y', 'gyro_z']) if graph_type == "scatter" else \
              px.histogram(data_subset, x=['gyro_x', 'gyro_y', 'gyro_z'])
    else:
        fig = px.line(data_subset, x='timestamp', y=axis) if graph_type == "line" else \
              px.scatter(data_subset, x='timestamp', y=axis) if graph_type == "scatter" else \
              px.histogram(data_subset, x=axis)

    # Create data summary table
    summary = data_subset.describe().to_html()

    return fig, summary

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
