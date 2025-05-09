from dash import Input, Output
import plotly.express as px
from src.data_loader import prepare_data
from src.constants import FILE_PATH

df = prepare_data(FILE_PATH)

def register_callbacks(app):
    @app.callback(
        Output('pie-chart', 'figure'),
        Output('bar-chart', 'figure'),
        Input('world-map', 'clickData')
    )
    def update_charts(clickData):
        if clickData is None:
            return {}, {}

        country = clickData['points'][0]['location']
        filtered = df[df['country_txt'] == country]

        if filtered.empty:
            return {}, {}

        #another random color sequence
        pie_colors = [
            "#d9d9d9",  # light grey
            "#f4a6a6",  # pale rose
            "#e06666",  # soft red
            "#cc3c3c",  # mid red
            "#a31515",  # strong red
            "#7e1416"   # velvet/dark red
        ]


        
        # PIE: Different attack types
        pie_data = filtered.groupby('attacktype1_txt').size().reset_index(name='count')
        pie_fig = px.pie(pie_data, names='attacktype1_txt', values='count',
                         title=f"Attack Types in {country}",
                         color_discrete_sequence=pie_colors)

        #black background
        pie_fig.update_layout(
        paper_bgcolor='#3a3a3f',
        plot_bgcolor='#3a3a3f',
        font_color='white'
    )

        # BAR: Number of attacks per year
        bar_data = filtered.groupby('iyear').size().reset_index(name='count')
        bar_fig = px.bar(bar_data, x='iyear', y='count',
                         title=f"Attacks per Year in {country}",
                         color_discrete_sequence=["#7e1416"])
        
        bar_fig.update_layout(
        paper_bgcolor='#3a3a3f',
        plot_bgcolor='#3a3a3f',
        font_color='white'
    )

        return pie_fig, bar_fig
