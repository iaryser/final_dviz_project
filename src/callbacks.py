from dash import Input, Output
import plotly.express as px
from src.data_loader import prepare_data
from src.config import FILE_PATH, TARGET_TYPE_DROPDOWN_ID, BAR_CHART_ID, PIE_CHART_ID, MAP_ID

df = prepare_data(FILE_PATH)

def register_callbacks(app):
    @app.callback(
        Output(TARGET_TYPE_DROPDOWN_ID, 'options'),
        Output(TARGET_TYPE_DROPDOWN_ID, 'value'),
        Input(MAP_ID, 'clickData')
    )
    def update_target_type_dropdown(clickData):
        if clickData:
            country = clickData['points'][0]['location']
            filtered_df = df[df['country_txt'] == country]
        else:
            filtered_df = df

        available_types = filtered_df['targtype1_txt'].dropna().unique()

        options = [{'label': t, 'value': t} for t in sorted(available_types)]

        return options, None

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
            "#fbeaea",  # very pale pink
            "#f4c6c6",  # blush pink
            "#f4a6a6",  # pale rose
            "#e06666",  # soft red
            "#d24c4c",  # mid soft red
            "#cc3c3c",  # mid red
            "#a31515",  # strong red
            "#7e1416"   # velvet/dark red
        ]

        # PIE: Different attack types
        pie_data = filtered_df.groupby('attacktype1_txt').size().reset_index(name='count')
        pie_data = pie_data.sort_values(by='count', ascending=False).reset_index(drop=True)

        pie_fig = px.pie(
            pie_data,
            names='attacktype1_txt',
            values='count',
            title=f"Attack Types in {country}",
            color_discrete_sequence=pie_colors[::-1]
        )

        pie_fig.update_traces(hovertemplate='%{label}<br>%{value:,.0f}<extra></extra>')

        # black background
        pie_fig.update_layout(
            paper_bgcolor='#3a3a3f',
            plot_bgcolor='#3a3a3f',
            font_color='white',
            title_font=dict(
            size=18,
            color='#d9d9d9',
            family='Arial, sans-serif'
            ))

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

        bar_fig.update_traces(hovertemplate='%{label}<br>%{value:,.0f}<extra></extra>')

        bar_fig.update_layout(
            paper_bgcolor='#3a3a3f',
            plot_bgcolor='#3a3a3f',
            font_color='white',
            title_font=dict(
            size=18,
            color='#d9d9d9',
            family='Arial, sans-serif'
        ))

        return pie_fig, bar_fig
