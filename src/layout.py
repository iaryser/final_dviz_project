import plotly.express as px
from dash import html, dcc
from src.data_loader import prepare_data

# Daten vorbereiten
df = prepare_data()

# Angriffe pro Land zählen
country_counts = df.groupby("country_txt").size().reset_index(name="attack_count")


#own colorscale bc default ones suck (this still sucks)
custom_colorscale = [
    [0.0, "#f3c6ff"],   # pale lavender
    [0.15, "#e100ff"],  # bright neon purple
    [0.3, "#b300cc"],   # medium
    [0.5, "#8000aa"],   # rich mid-purple
    [0.7, "#5e0099"],   # deep violet
    [1.0, "#3a0066"]    # dark purple (not black)
]

# Create map
map_fig = px.choropleth(
    country_counts,
    locations="country_txt",
    locationmode="country names",
    color="attack_count",
    color_continuous_scale=custom_colorscale,
    title="Global Terrorist attacks"
)


map_fig.update_geos(showframe=False, showcoastlines=False)
map_fig.update_layout(
    geo=dict(
        projection_type="natural earth",
        projection_scale=1.2,
        center={"lat": 20, "lon": 0},
        showcountries=True,
        bgcolor='#000000'
    ),
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    autosize=True
)

#dark theme bc swag
map_fig.update_layout(
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font_color='white'
)



# export layout
layout = html.Div([
    html.H1("Global Terrorism Dashboard", style={'color': 'white'}),

    dcc.Graph(id='world-map', figure=map_fig, style={'height': '80vh'}),
    
    html.Div([
        dcc.Graph(id='bar-chart', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='pie-chart', style={'width': '50%', 'display': 'inline-block'})
    ], style={'display': 'flex'})
],
style={
    'backgroundColor': '#000000',
    'padding': '20px',
    'minHeight': '100vh'
})

