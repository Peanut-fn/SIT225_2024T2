from paho.mqtt.client import Client as PahoClient

# Create your own Paho client with custom keepalive:
mqtt_client = PahoClient(client_id="", clean_session=True, userdata=None, protocol=None)
mqtt_client.keep_alive = 300  # e.g. 5 minutes
client._mqtt_client = mqtt_client  # inject into ArduinoCloudClient internals
import warnings, logging, time
from threading import Thread
from datetime import datetime
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
from arduino_iot_cloud import ArduinoCloudClient
from paho.mqtt.client import Client as PahoClient

# 1) Silence Python 3.13 date‐parsing warnings
warnings.filterwarnings(
    "ignore",
    message="Parsing dates involving a day of month without a year specified is ambiguous"
)

# 2) Your credentials
DEVICE_ID  = "fd25f63b-5b41-479a-a662-7aa791c097c1"
SECRET_KEY = "XSNHOOsCM?mDokja4DhYfsVq?"

# 3) Init ArduinoCloudClient
client = ArduinoCloudClient(
    device_id=DEVICE_ID,
    username=DEVICE_ID,
    password=SECRET_KEY
)

# 4) Tweak underlying MQTT keep-alive
mqtt_client = PahoClient()
mqtt_client._keepalive = 300            # 5 min keep-alive :contentReference[oaicite:11]{index=11}
client._mqtt_client = mqtt_client       # inject custom Paho client

# 5) Register variables
for v in ("py_x","py_y","py_z"):
    client.register(v)

buffer_in, N = [], 1000

# 6) Streaming with auto-reconnect
def streaming_thread():
    backoff = 1
    while True:
        try:
            client.start()
            while True:
                x, y, z = client["py_x"], client["py_y"], client["py_z"]
                buffer_in.append((x, y, z))
                time.sleep(0.01)
        except Exception as e:
            logging.warning(f"Stream drop: {e}; retrying in {backoff}s")
            time.sleep(backoff)
            backoff = min(backoff*2, 60)

Thread(target=streaming_thread, daemon=True).start()

# 7) Dash app
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Accelerometer Data"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='interval', interval=1000, n_intervals=0),
])

@app.callback(Output('live-graph','figure'), Input('interval','n_intervals'))
def update_graph(n):
    if len(buffer_in)>=N:
        batch = buffer_in[:N]; del buffer_in[:N]
        df = pd.DataFrame(batch, columns=["x","y","z"])
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        df.to_csv(f"week-8/data/accel_{ts}.csv", index=False)
        fig = go.Figure()
        for ax in ["x","y","z"]:
            fig.add_trace(go.Scatter(y=df[ax], mode='lines', name=f"{ax.upper()}-axis"))
        return fig.update_layout(title=f"Accel Batch @ {n}s")
    return go.Figure()

if __name__=='__main__':
    app.run(debug=True)  # per Dash 3.x :contentReference[oaicite:12]{index=12}
