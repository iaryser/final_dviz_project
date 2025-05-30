from dash import html, dcc
from src.config import TARGET_TYPE_DROPDOWN_ID, ATTACK_TYPE_DROPDOWN_ID, MAP_ID, BAR_CHART_ID, DONUT_CHART_ID, SELECTED_COUNTRY_STORE, COUNTRY_RESET_BUTTON_ID

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

        html.Br(),
        html.Br(),

        html.Label(
            "Target Type",
            style={'color': 'white',
                   'fontSize': '18px',
                   'fontWeight': 'bold',
                   'marginBottom': '5px',
                   'display': 'block'}
        ),

        dcc.Dropdown(
            id=TARGET_TYPE_DROPDOWN_ID,
            options=[],
            value=None,
            clearable=True,
            style={
                'backgroundColor': '#4c4c53',
            }
        ),

        html.Br(),
        html.Br(),

        html.Label(
            "Attack Types",
            style={'color': 'white',
                   'fontSize': '18px',
                   'fontWeight': 'bold',
                   'marginBottom': '5px',
                   'display': 'block'
                   }
        ),


        dcc.Checklist(
            id=ATTACK_TYPE_DROPDOWN_ID,
            options=[],
            style={'maxHeight': '300px'},
            labelStyle={'color': '#d9d9d9'},
        ),

        html.Button(
            'Reset Country',
            id=COUNTRY_RESET_BUTTON_ID,
            n_clicks=0,
            style={'marginTop': '15px',
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
        html.P([
        "Click on a country to view a timeline of total attacks and the distribution of attack types for that country.",
        html.Br(),
        "Use the legend on the right to filter visible countries by attacks per million."],
        style={'textAlign': 'center', 'color': '#d9d9d9', 'fontSize': '22px'}),

        dcc.Graph(id=MAP_ID, style={'height': '50vh', 'marginTop': '-20px'}, config=modeBar_config),

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
    'background-color': '#3a3a3f',
    'padding': '20px',
    'minHeight': '100vh'
})
