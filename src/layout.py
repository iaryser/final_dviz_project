from dash import html, dcc
from src.config import (
    TARGET_TYPE_DROPDOWN_ID,
    ATTACK_TYPE_DROPDOWN_ID,
    MAP_ID,
    BAR_CHART_ID,
    DONUT_CHART_ID,
    SELECTED_COUNTRY_STORE,
    COUNTRY_RESET_BUTTON_ID
)

# A config for the graphs to remove certain mode bar items
modeBar_config = {
    'displayModeBar': True,
    'modeBarButtonsToRemove': [
        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d',
        'zoomOut2d', 'autoScale2d', 'hoverClosestGeo',
        'hoverClosestCartesian', 'hoverCompareCartesian', 'toImage'
    ],
    'displaylogo': False
}

# Sidebar layout: filters and reset button
sidebar = html.Div([
    html.H1("Global Terrorism Dashboard", style={'color': 'white'}),

    # Dropdown to filter by target type
    html.Label("Target Type", style={
        'color': 'white',
        'fontSize': '18px',
        'fontWeight': 'bold'
    }),

    dcc.Dropdown(
        id=TARGET_TYPE_DROPDOWN_ID,
        options=[],
        value=None,
        clearable=True,
        style={
            'backgroundColor': '#4c4c53',
            'marginTop': '-5px'
        }
    ),

    # Checklist to filter by attack types
    html.Label("Attack Types", style={
        'color': 'white',
        'fontSize': '18px',
        'fontWeight': 'bold',
        'marginTop': '10px'
    }),

    dcc.Checklist(
        id=ATTACK_TYPE_DROPDOWN_ID,
        options=[],
        style={'maxHeight': '300px', 'overflowY': 'auto'},
        labelStyle={
            'color': '#d9d9d9',
            'display': 'block',
            'marginBottom': '6px'
        }
    ),

    # Button to clear the currently selected country
    html.Button(
        'Reset Country',
        id=COUNTRY_RESET_BUTTON_ID,
        n_clicks=0,
        style={
            'marginTop': '15px',
            'backgroundColor': '#4c4c53',
            'color': 'white',
            'border': 'none',
            'padding': '10px 15px',
            'borderRadius': '6px',
            'cursor': 'pointer',
            'boxShadow': '2px 2px 10px rgba(0,0,0,0.4)',
            'marginBottom': 'auto'
        }
    )
], style={
    'width': '20%',
    'height': '87.5vh',
    'overflowY': 'auto',
    'position': 'fixed',
    'padding': '25px',
    'backgroundColor': '#2e2e33',
    'border': '2px solid #444',
    'boxShadow': '0 0 10px 4px rgba(0,0,0,0.2)',
    'borderRadius': '8px',
    'display': 'flex',
    'flexDirection': 'column',
    'gap': '16px',
    'zIndex': '10'
})

# Main dashboard content: map, bar chart, donut chart
main_content = html.Div([
    # Description text
    html.P([
        "Click on a country to view a timeline of total attacks and the distribution of attack types for that country.",
        html.Br(),
        "Use the legend on the right to filter visible countries by attacks per million."
    ], style={
        'textAlign': 'center',
        'color': '#d9d9d9',
        'fontSize': '22px',
    }),

    # World map graph
    dcc.Graph(
        id=MAP_ID,
        style={'height': '50vh', 'marginTop': '-20px'},
        config=modeBar_config
    ),

    # Side-by-side bar chart and donut chart
    html.Div([
        dcc.Graph(
            id=BAR_CHART_ID,
            style={'width': '50%', 'height': '50vh'},
            config=modeBar_config
        ),
        dcc.Graph(
            id=DONUT_CHART_ID,
            style={'width': '50%', 'height': '50vh'},
            config={"displayModeBar": False}
        )
    ], style={'display': 'flex'})
], style={
    'width': '75%',
    'marginLeft': '25%',
    'height': '100vh',
    'display': 'inline-block'
})

# Entire layout with a dark background and data store
layout = html.Div([
    dcc.Store(id=SELECTED_COUNTRY_STORE, data=None),

    sidebar,

    main_content
], style={
    'backgroundColor': '#3a3a3f',
    'padding': '20px',
    'minHeight': '100vh'
})
