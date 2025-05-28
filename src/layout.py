from dash import html, dcc
from src.data_loader import prepare_data, download_data, get_country_counts
from src.config import *
from src.charts.map_plot import create_map

# Download data
download_data(FOLDER_PATH, FILE_NAME)

# Daten vorbereiten
df = prepare_data(FILE_PATH)

country_counts, labels = get_country_counts(df)

# Create map
map_fig = create_map(country_counts, labels)

modeBar_config = {
    'displayModeBar': True,
    'modeBarButtonsToRemove': [
        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d',
        'zoomOut2d', 'autoScale2d', 'hoverClosestGeo',
        'hoverClosestCartesian', 'hoverCompareCartesian', 'toImage'
    ],
    'displaylogo': False
}

# Layout Dash
layout = html.Div([
    html.H1("Global Terrorism Dashboard", style={'color': 'white'}),
    dcc.Graph(id=MAP_ID, figure=map_fig, style={
              'height': '80vh'}, config=modeBar_config),

    html.Div([
        html.Div([
            html.Label(
                "Select Target Type:",
                style={
                    'color': '#d9d9d9',
                    'fontSize': '20px',
                    'fontWeight': 'bold'
                }
            ),
            dcc.Dropdown(
                id=TARGET_TYPE_DROPDOWN_ID,
                options=[],
                value=None,
                clearable=True,
                style={
                    'backgroundColor': '#4c4c53',
                    'color': 'black'
                }
            )
        ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
        html.Div([
            html.Label(
                "Select the Attack Types you want to be displayed in the chart below.",
                style={'color': '#d9d9d9'}
            ),
            dcc.Dropdown(
                id=ATTACK_TYPE_DROPDOWN_ID,
                value=None,
                clearable=True,
                multi=True,
                style={
                    'backgroundColor': '#4c4c53',
                    'color': 'black'
                }
            )
        ], style={'width': '48%', 'display': 'inline-block'})
    ], style={'marginBottom': '20px'}),

    html.Div([
        dcc.Graph(id=BAR_CHART_ID, style={
                  'width': '50%', 'display': 'inline-block'}, config=modeBar_config),
        dcc.Graph(id=DONUT_CHART_ID, style={
                  'width': '50%', 'display': 'inline-block'}, config={"displayModeBar": False})
    ], style={'display': 'flex'})
], style={
    'backgroundColor': '#3a3a3f',
    'padding': '20px',
    'minHeight': '100vh'
})
