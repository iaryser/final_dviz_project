import plotly.express as px
from dash import html, dcc
from src.data_loader import prepare_data, download_data
from src.constants import FOLDER_PATH, FILE_NAME, FILE_PATH

# Download data
download_data(FOLDER_PATH, FILE_NAME)

# Daten vorbereiten
df = prepare_data(FILE_PATH)

# Angriffe pro Land zählen
country_counts = df.groupby("country_txt").size().reset_index(name="attack_count")


#own colorscale bc default ones suck (this still sucks)
custom_colorscale = [
    [0.0, "#d9d9d9"],   # light grey
    [0.15, "#f4a6a6"],  # pale rose
    [0.3, "#e06666"],   # soft red
    [0.5, "#cc3c3c"],   # mid red
    [0.7, "#a31515"],   # intense red
    [1.0, "#7e1416"]    # velvet/dark red
]


# Create map
map_fig = px.choropleth(
    country_counts,
    locations="country_txt",
    locationmode="country names",
    color="attack_count",
    color_continuous_scale=custom_colorscale,
    title="Global Terrorist attacks",
    range_color=[0, 5000]
)


# Geo-Settings
map_fig.update_geos(
    showframe=False,
    showcoastlines=False
)

# Dark Design & Tooltyp styling
map_fig.update_traces(
    hovertemplate=(
        "<b>%{location}</b><br>"
        "Attacks: %{z:,}<br>"
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

# Layout Dash
layout = html.Div([
    html.H1("Global Terrorism Dashboard", style={'color': 'white'}),
    dcc.Graph(id='world-map', figure=map_fig, style={'height': '80vh'}),
    html.Div([
        dcc.Graph(id='bar-chart', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='pie-chart', style={'width': '50%', 'display': 'inline-block'})
    ], style={'display': 'flex'})
], style={
    'backgroundColor': '#3a3a3f',
    'padding': '20px',
    'minHeight': '100vh'
})
