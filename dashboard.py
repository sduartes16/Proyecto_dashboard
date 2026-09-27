"""Dashboard interactivo de retrasos de vuelos (tarea).

Ejecutar en desarrollo:
    python dashboard.py        ->  http://127.0.0.1:8050

Ejecutar en produccion (lo hace la plataforma de despliegue):
    gunicorn dashboard:server  ->  usa el objeto WSGI `server` de este modulo
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
from dash import Dash, Input, Output, dcc, html

# --------------------------------------------------------------------- datos
# Los datos viajan CON el repositorio y se leen desde la carpeta del archivo.
# NO uses rutas absolutas: en el servidor las rutas son distintas.
DATA_FILE = Path(__file__).with_name("airline_data.csv")

df = pd.read_csv(
    DATA_FILE,
    encoding="ISO-8859-1",
    # Estos campos traen ceros a la izquierda: deben leerse como texto.
    dtype={
        "Div1Airport": str,
        "Div1TailNum": str,
        "Div2Airport": str,
        "Div2TailNum": str,
    },
)

app = Dash(__name__)

# -------------------------------------------------------------------- layout
# TODO 1

app.layout = html.Div(children=[
    html.H1(
        "Flight Delay Time Statistics Dashboard",
        style={"textAlign": "center"}
    ),

    html.Div([
        html.Label("Ingrese el año: "),
        dcc.Input(
            id="input-year",
            type="number",
            value=2010
        )
    ]),

    html.Div([
        dcc.Graph(id="carrier-plot"),
        dcc.Graph(id="weather-plot")
    ], style={"display": "flex"}),

    html.Div([
        dcc.Graph(id="nas-plot"),
        dcc.Graph(id="security-plot")
    ], style={"display": "flex"}),

    html.Div([
        dcc.Graph(id="late-plot")
    ], style={"display": "flex"})
])


# ------------------------------------------------------------------ calculos
# TODO 2

def compute_info(datos, entered_year):

    datos_year = datos[datos["Year"] == entered_year]

    avg_car = (
        datos_year
        .groupby(["Month", "Reporting_Airline"])["CarrierDelay"]
        .mean()
        .reset_index()
    )

    avg_weather = (
        datos_year
        .groupby(["Month", "Reporting_Airline"])["WeatherDelay"]
        .mean()
        .reset_index()
    )

    avg_NAS = (
        datos_year
        .groupby(["Month", "Reporting_Airline"])["NASDelay"]
        .mean()
        .reset_index()
    )

    avg_security = (
        datos_year
        .groupby(["Month", "Reporting_Airline"])["SecurityDelay"]
        .mean()
        .reset_index()
    )

    avg_late = (
        datos_year
        .groupby(["Month", "Reporting_Airline"])["LateAircraftDelay"]
        .mean()
        .reset_index()
    )

    return avg_car, avg_weather, avg_NAS, avg_security, avg_late


# ------------------------------------------------------------------ callback
# TODO 3

@app.callback(
    Output("carrier-plot", "figure"),
    Output("weather-plot", "figure"),
    Output("nas-plot", "figure"),
    Output("security-plot", "figure"),
    Output("late-plot", "figure"),
    Input("input-year", "value")
)
def get_graph(entered_year):

    if entered_year is None:
        fig = Figure()
        fig.update_layout(title="Ingrese un año")
        return fig, fig, fig, fig, fig

    try:
        entered_year = int(entered_year)
    except (TypeError, ValueError):
        fig = Figure()
        fig.update_layout(title="Ingrese un año válido")
        return fig, fig, fig, fig, fig

    avg_car, avg_weather, avg_NAS, avg_security, avg_late = compute_info(
        df, entered_year
    )

    if avg_car.empty:
        fig = Figure()
        fig.update_layout(
            title=f"No hay datos disponibles para el año {entered_year}"
        )
        return fig, fig, fig, fig, fig

    fig_car = px.line(
        data_frame=avg_car,
        x="Month",
        y="CarrierDelay",
        color="Reporting_Airline",
        title="Promedio de retraso por transportista",
        labels={
            "CarrierDelay": "Carrier Delay (minutes)",
            "Month": "Month"
        }
    )

    fig_weather = px.line(
        data_frame=avg_weather,
        x="Month",
        y="WeatherDelay",
        color="Reporting_Airline",
        title="Promedio de retraso por clima",
        labels={
            "WeatherDelay": "Weather Delay (minutes)",
            "Month": "Month"
        }
    )

    fig_NAS = px.line(
        data_frame=avg_NAS,
        x="Month",
        y="NASDelay",
        color="Reporting_Airline",
        title="Promedio de retraso por NAS",
        labels={
            "NASDelay": "NAS Delay (minutes)",
            "Month": "Month"
        }
    )

    fig_security = px.line(
        data_frame=avg_security,
        x="Month",
        y="SecurityDelay",
        color="Reporting_Airline",
        title="Promedio de retraso por seguridad",
        labels={
            "SecurityDelay": "Security Delay (minutes)",
            "Month": "Month"
        }
    )

    fig_late = px.line(
        data_frame=avg_late,
        x="Month",
        y="LateAircraftDelay",
        color="Reporting_Airline",
        title="Promedio de retraso por aeronave tardía",
        labels={
            "LateAircraftDelay": "Late Aircraft Delay (minutes)",
            "Month": "Month"
        }
    )

    return fig_car, fig_weather, fig_NAS, fig_security, fig_late

# --------------------------------------------------------------- produccion
# RF9: objeto WSGI que consumira gunicorn. gunicorn IMPORTA este modulo y
# busca una variable llamada `server`; nunca ejecuta el bloque __main__.
server = app.server

if __name__ == "__main__":
    # debug=True recarga el servidor al guardar: comodo en desarrollo,
    # y NUNCA se usa en produccion.
    app.run(debug=True, port=8050)
