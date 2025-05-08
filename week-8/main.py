# -*- coding: utf-8 -*-

# Import necessary libraries
from arduino_iot_cloud import ArduinoCloudClient
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import datetime
import os
import threading
import time
import collections # Can be useful for fixed-size buffers, but lists are used here as per hint

# --- Arduino Cloud Configuration ---
# IMPORTANT: Replace with your actual Device ID and Secret Key obtained
# from setting up the "Third Party Device" or "Python Script" Thing in Arduino Cloud.
DEVICE_ID = "YOUR_DEVICE_ID"
SECRET_KEY = "YOUR_SECRET_KEY"

# Initialize the Arduino Cloud client. This needs to be done before
# defining variables if using the @client.on_property decorators.
client = ArduinoCloudClient(DEVICE_ID, SECRET_KEY)

# --- Data Buffering Configuration (Steps 4 & 6) ---
# N_SAMPLES defines the block size of data to process, display, and save at once.
# The task suggests N=1000 for ~10 seconds of data. Adjust this value based on
# your phone's accelerometer sampling rate to get approximately 10 seconds.
# If your phone sends data at ~100Hz, N_SAMPLES = 1000 is appropriate.
N_SAMPLES = 1000

# Buffer to receive incoming data from the Arduino Cloud.
# Data is continuously appended to these lists as it arrives.
incoming_buffer_x = []
incoming_buffer_y = []
incoming_buffer_z = []
incoming_buffer_time = [] # Store timestamps corresponding to incoming data

# Buffer to hold the specific block of N_SAMPLES that is currently being
# displayed on the Dash graph and saved to files.
display_buffer_x = []
display_buffer_y = []
display_buffer_z = []
display_buffer_time = []

# --- Arduino Cloud Variable Callbacks (Receiving Data - Part of Step 3/4) ---
# These functions are automatically called by the ArduinoCloudClient
# whenever a new value is received for the linked variables (py_x, py_y, py_z)
# from the Arduino Cloud.

@client.on_property("py_x")
def on_py_x_change(value):
    """Callback function triggered when py_x variable receives data."""
    # Access global buffer lists to modify them
    global incoming_buffer_x, incoming_buffer_y, incoming_buffer_z, incoming_buffer_time

    # Append the new accelerometer value and the current timestamp to the incoming buffers.
    # We append the timestamp here assuming x, y, and z values for a single reading
    # arrive very close together in time.
    incoming_buffer_x.append(value)
    incoming_buffer_time.append(datetime.datetime.now())
    # print(f"Received py_x: {value} at {incoming_buffer_time[-1]}") # Optional: print to console

@client.on_property("py_y")
def on_py_y_change(value):
    """Callback function triggered when py_y variable receives data."""
    global incoming_buffer_y
    incoming_buffer_y.append(value)
    # print(f"Received py_y: {value}") # Optional

@client.on_property("py_z")
def on_py_z_change(value):
    """Callback function triggered when py_z variable receives data."""
    global incoming_buffer_z
    incoming_buffer_z.append(value)
    # print(f"Received py_z: {value}") # Optional


# --- Data Processing & Buffer Management (Step 6) ---
def process_buffer():
    """
    Checks if the incoming buffer contains at least N_SAMPLES.
    If yes, it copies the first N_SAMPLES to the display buffer,
    removes those samples from the incoming buffer, and returns True.
    Otherwise, it returns False.
    This function ensures that the data used for plotting and saving
    is a distinct block of N_SAMPLES.
    """
    global incoming_buffer_x, incoming_buffer_y, incoming_buffer_z, incoming_buffer_time
    global display_buffer_x, display_buffer_y, display_buffer_z, display_buffer_time

    # Determine the minimum length across all incoming buffers.
    # This helps handle cases where x, y, z might not arrive in perfect sync.
    min_len = min(len(incoming_buffer_x), len(incoming_buffer_y), len(incoming_buffer_z), len(incoming_buffer_time))

    # Check if we have enough samples to process a block
    if min_len >= N_SAMPLES:
        print(f"Processing {N_SAMPLES} samples from incoming buffer...")
        # Copy the first N_SAMPLES from incoming to display buffers
        display_buffer_x = incoming_buffer_x[:N_SAMPLES]
        display_buffer_y = incoming_buffer_y[:N_SAMPLES]
        display_buffer_z = incoming_buffer_z[:N_SAMPLES]
        display_buffer_time = incoming_buffer_time[:N_SAMPLES]

        # Remove the samples that were just moved to the display buffer
        # from the incoming buffer.
        incoming_buffer_x = incoming_buffer_x[N_SAMPLES:]
        incoming_buffer_y = incoming_buffer_y[N_SAMPLES:]
        incoming_buffer_z = incoming_buffer_z[N_SAMPLES:]
        incoming_buffer_time = incoming_buffer_time[N_SAMPLES:]

        print("Buffer processed. New data block ready for graph and saving.")
        return True # Indicate that a new block of data was processed
    else:
        # print(f"Incoming buffer size: {min_len}/{N_SAMPLES}. Waiting for more data.") # Optional status print
        return False # Indicate that no new block was processed


# --- File Saving (Step 7) ---
# Create a directory to store saved data and plots.
# This directory name matches the requirement for GitHub submission.
SAVE_DIR = 'week-8_data'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
    print(f"Created directory: {SAVE_DIR}")

def save_data_and_plot(data_x, data_y, data_z, data_time):
    """
    Saves the data from the current display buffer to a CSV file
    and saves the corresponding Plotly figure as PNG and HTML files.
    Filenames are based on a timestamp.
    """
    if not data_time: # Prevent saving if the display buffer is empty
        print("Display buffer is empty, nothing to save.")
        return

    # Generate a timestamp string for the filename.
    # Using the timestamp of the last data point in the buffer is a common approach.
    timestamp_str = data_time[-1].strftime("%Y%m%d_%H%M%S")
    filename_base = os.path.join(SAVE_DIR, f"activity_{timestamp_str}")

    print(f"Attempting to save data and plot with base filename: {filename_base}")

    # Save data to CSV file using Pandas DataFrame
    try:
        df = pd.DataFrame({
            'Timestamp': data_time,
            'Accel_X': data_x,
            'Accel_Y': data_y,
            'Accel_Z': data_z
        })
        csv_filepath = f"{filename_base}.csv"
        df.to_csv(csv_filepath, index=False)
        print(f"Successfully saved data to {csv_filepath}")
    except Exception as e:
        print(f"Error saving CSV data to {filename_base}.csv: {e}")


    # Create a Plotly figure object from the data in the display buffer.
    # This figure will be saved.
    fig_save = go.Figure()
    fig_save.add_trace(go.Scattergl(x=data_time, y=data_x, mode='lines', name='Accel X'))
    fig_save.add_trace(go.Scattergl(x=data_time, y=data_y, mode='lines', name='Accel Y'))
    fig_save.add_trace(go.Scattergl(x=data_time, y=data_z, mode='lines', name='Accel Z'))

    # Configure the layout for the saved plot
    fig_save.update_layout(
        title=f'Accelerometer Data ({len(data_time)} samples) - {timestamp_str}',
        xaxis_title='Time',
        yaxis_title='Acceleration (g?)', # Units are typically in 'g' for smartphone accelerometers
        hovermode='x unified' # Improve hover experience
        # You could add fixed y-axis ranges here if you want consistent plot scales
        # yaxis=dict(range=[-5, 5]) # Example range, adjust based on expected values
    )

    # Save the figure as a static PNG image. Requires the 'kaleido' library.
    try:
        png_filepath = f"{filename_base}.png"
        fig_save.write_image(png_filepath)
        print(f"Successfully saved plot to {png_filepath} (PNG)")
    except Exception as e:
        print(f"Could not save plot as PNG to {filename_base}.png. Make sure 'kaleido' is installed (`pip install kaleido`). Error: {e}")

    # Save the figure as an interactive HTML file.
    try:
        html_filepath = f"{filename_base}.html"
        fig_save.write_html(html_filepath)
        print(f"Successfully saved plot to {html_filepath} (HTML)")
    except Exception as e:
         print(f"Could not save plot as HTML to {filename_base}.html: {e}")


# --- Plotly Dash Web Application Setup (Step 4/5) ---
# Initialize the Dash application
app = dash.Dash(__name__)

# Define the layout of the Dash web page.
# This structure includes a title, the graph component, an interval component
# to trigger updates, and a text area to display buffer status.
app.layout = html.Div(style={'textAlign': 'center', 'fontFamily': 'sans-serif'}, children=[
    html.H1("Live Smartphone Accelerometer Data Stream"),

    # The dcc.Graph component displays the Plotly figure.
    # It's updated via the callback function.
    dcc.Graph(
        id='live-update-graph',
        # Initial figure displayed when the app starts.
        figure=go.Figure(layout=go.Layout(
            title='Waiting for data...',
            xaxis_title='Time',
            yaxis_title='Acceleration'
        ))
    ),

    # The dcc.Interval component triggers the callback function periodically.
    # The 'interval' property is in milliseconds. Adjust this to control
    # how often the buffer is checked and the graph *potentially* updated.
    # The graph only updates visually when process_buffer() returns True.
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000, # Check buffer status every 1 second (1000 ms)
        n_intervals=0 # Initial value, increases automatically
    ),

    # A simple Div to display the current status of the incoming buffer.
    html.Div(id='buffer-status-display', style={'marginTop': '20px', 'fontSize': '1.1em'})
])

# --- Dash Callback for Graph Updates (Step 5) ---
# This callback function is triggered by the 'n_intervals' property
# of the 'interval-component' every time the interval elapses.
@app.callback(Output('live-update-graph', 'figure'), # Output: Update the 'figure' property of 'live-update-graph'
              Output('buffer-status-display', 'children'), # Output: Update the 'children' (text) of 'buffer-status-display'
              Input('interval-component', 'n_intervals')) # Input: Triggered by the 'n_intervals' of 'interval-component'
def update_graph_live(n):
    """
    This function is called periodically by Dash. It processes the incoming
    data buffer, saves data/plots if a new block is ready, and updates
    the displayed graph.
    """
    global display_buffer_x, display_buffer_y, display_buffer_z, display_buffer_time
    global incoming_buffer_time # Used for checking incoming buffer size for status display

    # Attempt to process the incoming data buffer.
    # This will update display_buffer_* if N_SAMPLES are available.
    data_processed = process_buffer()

    # Get the current length of the incoming buffer for displaying status.
    current_buffer_len = min(len(incoming_buffer_x), len(incoming_buffer_y), len(incoming_buffer_z), len(incoming_buffer_time))
    status_text = f"Incoming buffer size: {current_buffer_len}/{N_SAMPLES} samples. "

    # Create the Plotly figure to be displayed in the Dash app.
    # This figure is created using the data currently in the DISPLAY buffer.
    fig = go.Figure()
    if display_buffer_time: # Only add traces if the display buffer contains data
        fig.add_trace(go.Scattergl(x=display_buffer_time, y=display_buffer_x, mode='lines', name='Accel X'))
        fig.add_trace(go.Scattergl(x=display_buffer_time, y=display_buffer_y, mode='lines', name='Accel Y'))
        fig.add_trace(go.Scattergl(x=display_buffer_time, y=display_buffer_z, mode='lines', name='Accel Z'))

        # Update the layout of the displayed figure
        fig.update_layout(
            title=f'Live Accelerometer Data ({len(display_buffer_time)} samples displayed)',
            xaxis_title='Time',
            yaxis_title='Acceleration (g?)', # Adjust units if known
            # uirevision='constant' helps prevent the graph from resetting zoom/pan
            # every time it updates.
            uirevision='constant',
            hovermode='x unified'
            # xaxis=dict(range=[display_buffer_time[0], display_buffer_time[-1]]) # Optional: fix x-axis range to current window
        )
        status_text += f"Displaying {len(display_buffer_time)} samples."
    else:
         # Display a waiting message if the display buffer is empty
         fig.update_layout(title='Waiting for enough data to plot...', xaxis_title='Time', yaxis_title='Acceleration')
         status_text += "Display buffer empty."


    # If process_buffer() returned True, it means a new block of data was just
    # moved to the display buffer. This is the moment to save that block.
    if data_processed:
        save_data_and_plot(display_buffer_x, display_buffer_y, display_buffer_z, display_buffer_time)
        status_text += " Saved latest block."

    # Return the figure and the status text to update the Dash outputs.
    # If no new data was processed, the figure returned will be the same as
    # the last one, and Dash will efficiently not re-render it unless necessary.
    return fig, status_text


# --- Running the Arduino Cloud Client and Dash Server ---
# The Arduino Cloud client needs to run its communication loop continuously
# to receive data. The Dash web server also needs to run continuously
# to serve the web page and handle callbacks.
# To run both simultaneously, we start the Cloud client in a separate thread.

def run_client():
    """Function to connect the Arduino Cloud client and keep it running."""
    print("Connecting to Arduino Cloud...")
    try:
        # Connect to the Arduino Cloud using the provided credentials
        client.connect()
        print("Arduino Cloud client connected successfully.")
        # loop_forever() keeps the client connected and processes incoming messages.
        # This function blocks, which is why it's run in a separate thread.
        client.loop_forever()
    except Exception as e:
        # Basic error handling for connection issues.
        print(f"Arduino Cloud connection error: {e}")
        print("Attempting to reconnect in 5 seconds...")
        time.sleep(5)
        run_client() # Recursive call to attempt reconnection


if __name__ == '__main__':
    # This block executes when the script is run directly.

    # Start the Arduino Cloud client in a separate daemon thread.
    # A daemon thread runs in the background and exits automatically
    # when the main program (the Dash server) exits.
    client_thread = threading.Thread(target=run_client)
    client_thread.daemon = True # Set as daemon thread
    client_thread.start() # Start the thread

    # Give the client thread a moment to establish connection before
    # starting the Dash server. This is optional but can help avoid
    # errors if the Dash app tries to access variables before the client is ready.
    time.sleep(2)

    # Start the Dash web server. This function blocks and runs the web app.
    # debug=True is useful for development: provides a debugger in the browser
    # and automatically reloads the app when code changes. Set to False for production.
    print("Starting Dash server...")
    app.run_server(debug=True) # Default port is 8050
