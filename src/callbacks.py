from dash import Input, Output
import plotly.express as px
from src.data_loader import prepare_data
from src.config import FILE_PATH, TARGET_TYPE_DROPDOWN_ID, BAR_CHART_ID, PIE_CHART_ID, MAP_ID

df = prepare_data(FILE_PATH)

def register_callbacks(app):
    @app.callback(
        Output(PIE_CHART_ID, 'figure'),
        Output(BAR_CHART_ID, 'figure'),
        Input(TARGET_TYPE_DROPDOWN_ID, 'value'),
        Input(MAP_ID, 'clickData')
    )
    def update_charts(selected_target_type, clickData):
        filtered_df = df.copy()
        if selected_target_type:
            filtered_df = filtered_df[
                filtered_df['targtype1_txt'] == selected_target_type
            ]

        if clickData:
            country = clickData['points'][0]['location']
            filtered_df = filtered_df[filtered_df['country_txt'] == country]
        else:
            country = 'Global'

        # another random color sequence
        pie_colors = [
            "#d9d9d9",  # light grey
            "#f4a6a6",  # pale rose
            "#e06666",  # soft red
            "#cc3c3c",  # mid red
            "#a31515",  # strong red
            "#7e1416"   # velvet/dark red
        ]

        # PIE: Different attack types
        pie_data = filtered_df.groupby(
            'attacktype1_txt').size().reset_index(name='count')
        pie_fig = px.pie(
            pie_data,
            names='attacktype1_txt',
            values='count',
            title=f"Attack Types in {country}",
            color_discrete_sequence=pie_colors
        )

        # black background
        pie_fig.update_layout(
            paper_bgcolor='#3a3a3f',
            plot_bgcolor='#3a3a3f',
            font_color='white'
        )

        # BAR: Number of attacks per year
        bar_data = filtered_df.groupby(
            'iyear').size().reset_index(name='count')
        bar_fig = px.bar(
            bar_data,
            x='iyear',
            y='count',
            title=f"Attacks per Year in {country}",
            color_discrete_sequence=["#7e1416"]
        )

        bar_fig.update_layout(
            paper_bgcolor='#3a3a3f',
            plot_bgcolor='#3a3a3f',
            font_color='white'
        )

        return pie_fig, bar_fig
