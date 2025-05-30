from dash import html, dcc
from src.data_loader import download_data
from src.config import FOLDER_PATH, TERRORISM_FILE, TARGET_TYPE_DROPDOWN_ID, ATTACK_TYPE_DROPDOWN_ID, MAP_ID, BAR_CHART_ID, DONUT_CHART_ID, SELECTED_COUNTRY_STORE, COUNTRY_RESET_BUTTON_ID

# Download data
download_data(FOLDER_PATH, TERRORISM_FILE)

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
    dcc.Store(id=SELECTED_COUNTRY_STORE, data=None),

    html.Div([
        html.H1("Global Terrorism Dashboard", style={'color': 'white'}),
        html.Label(
            "Target Type",
            style={'color': '#d9d9d9'}
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
        ),

        html.Br(),

        html.Label(
            "Attack Types",
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
        ),

        html.Br(),

        html.Button(
            'Reset Country',
            id=COUNTRY_RESET_BUTTON_ID,
            n_clicks=0,
            style={'marginTop': '10px',
                   'backgroundColor': '#444', 'color': 'white'}
        )
    ], style={
        'width': '20%',
        'height': '100vh',
        'position': 'fixed',
        'verticalAlign': 'top',
        'paddingRight': '2%'
    }),

    html.Div([
        dcc.Graph(id=MAP_ID, style={'height': '50vh'}, config=modeBar_config),

        html.Div([
            dcc.Graph(id=BAR_CHART_ID, style={
                'width': '50%', 'height': '50vh', 'display': 'inline-block'}, config=modeBar_config),
            dcc.Graph(id=DONUT_CHART_ID, style={
                'width': '50%', 'height': '50vh', 'display': 'inline-block'}, config={"displayModeBar": False})
        ], style={'display': 'flex'})
    ], style={
        'width': '75%',
        'display': 'inline-block',
        'marginLeft': '25%',
        'height': '100vh'
    })
], style={
    'backgroundColor': '#3a3a3f',
    'padding': '20px',
    'minHeight': '100vh'
})
