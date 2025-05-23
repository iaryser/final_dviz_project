import pandas as pd
import plotly.express as px
from dash import html, dcc
from src.data_loader import prepare_data, download_data
from src.config import *

# Download data
download_data(FOLDER_PATH, FILE_NAME)

# Daten vorbereiten
df = prepare_data(FILE_PATH)

# Angriffe pro Land zählen
country_counts = df.groupby(
    "country_txt").size().reset_index(name="attack_count")

#bin attack count into six categories
max_attacks = country_counts['attack_count'].max()
bins=[0, 250, 1215, 2743, 5235, 8306, max_attacks]
labels=['0-250', '251-1215', '1216-2743', '2744-5235', '5236-8306', '8307+' ]

country_counts['attack_bin'] = pd.cut(
    country_counts['attack_count'],
    bins=bins,
    labels=labels,
    include_lowest=True
)

#map each label to desired colorscale
hex_colors = ["#d9d9d9","#f4a6a6","#e06666","#cc3c3c","#a31515","#7e1416"]
color_map  = dict(zip(labels, hex_colors))


# Create map
map_fig = px.choropleth(
    country_counts,
    locations="country_txt",
    locationmode="country names",
    color="attack_bin",
    color_discrete_map=color_map,
    category_orders={'attack_bin': labels},
    labels={'attack_bin': 'Attack Range'},
    title="Global Terrorist attacks",
    custom_data=['attack_count']
)

map_fig.update_coloraxes(colorbar_title="Number of Attacks")

# Geo-Settings
map_fig.update_geos(
    showframe=False,
    showcoastlines=False
)

# Dark Design & Tooltyp styling
map_fig.update_traces(
    hovertemplate=(
        "<b>%{location}</b><br>"
        "Attacks: %{customdata[0]:,}<br>"
        "<extra></extra>"
    )
)

map_fig.update_layout(
    geo=dict(
        projection_type="natural earth",
        projection_scale=1.2,
        center={"lat": 20, "lon": 0},
        showcountries=True,
        bgcolor='#3a3a3f'
    ),
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    autosize=True,
    hoverlabel=dict(
        bgcolor="rgba(50,50,50,0.8)",
        font_size=13,
        font_family="Arial, sans-serif",
        font_color="white",
        bordercolor="#666"
    ),
    paper_bgcolor='#3a3a3f',
    plot_bgcolor='#3a3a3f',
    font_color='white'
)

map_fig.update_layout(
    legend=dict(
        title=dict(text="Attack Range", font=dict(size=18)),
        font=dict(size=14),
        itemwidth=50,
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    )
)

map_config = {
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
    dcc.Graph(id=MAP_ID, figure=map_fig, style={'height': '80vh'}, config=map_config),

    html.Div([
        html.Label("Select Target Type:",
                   style={
                       'color': 'white',
                       'fontSize': '20px',
                       'fontWeight': 'bold'
                   }),
        dcc.Dropdown(
            id=TARGET_TYPE_DROPDOWN_ID,
            options=[],
            value=None,
            clearable=True,
            style={  #styling the dropdown but to further refine well have to create an assets folder with custom css stuff: assets/custom.css
                'backgroundColor': '#4c4c53',
                'color': 'black'
            }
        )
    ], style={'width': '40%', 'marginBottom': '20px'}),  # moved here

    html.Div([
        dcc.Graph(id=BAR_CHART_ID, style={ 'width': '50%', 'display': 'inline-block' }, config={"displayModeBar": False}),
        dcc.Graph(id=PIE_CHART_ID, style={ 'width': '50%', 'display': 'inline-block' }, config={"displayModeBar": False})
    ], style={'display': 'flex'})
], style={
    'backgroundColor': '#3a3a3f',
    'padding': '20px',
    'minHeight': '100vh'
})