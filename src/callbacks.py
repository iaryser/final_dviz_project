from dash import Input, Output
from src.data_loader import get_dropdown_options, get_map_data, get_donut_data, get_bar_data
from src.config import TARGET_TYPE_DROPDOWN_ID, BAR_CHART_ID, DONUT_CHART_ID, MAP_ID, ATTACK_TYPE_DROPDOWN_ID
from src.charts.map_plot import create_map
from src.charts.bar_plot import create_bar_fig
from src.charts.donut_plot import create_donut_fig


def register_callbacks(app):
    @app.callback(
        Output(MAP_ID, 'figure'),
        Input(MAP_ID, 'clickData')
    )
    def update_map(clickData):
        highlight_country = clickData['points'][0]['location'] if clickData else None

        country_counts, labels = get_map_data()

        map_fig = create_map(country_counts, labels, highlight_country)

        return map_fig

    @app.callback(
        Output(TARGET_TYPE_DROPDOWN_ID, 'options'),
        Output(TARGET_TYPE_DROPDOWN_ID, 'value'),
        Input(MAP_ID, 'clickData')
    )
    def update_target_type_dropdown(clickData):
        if clickData:
            country = clickData['points'][0]['location']
            options = get_dropdown_options(
                'targtype1_txt', {'country_txt': country}
            )
        else:
            options = get_dropdown_options('targtype1_txt')

        return options, None

    @app.callback(
        Output(ATTACK_TYPE_DROPDOWN_ID, 'options'),
        Input(TARGET_TYPE_DROPDOWN_ID, 'value'),
        Input(MAP_ID, 'clickData')
    )
    def update_attack_type_dropdown(selected_target_type, clickData):
        filters = {}

        if selected_target_type:
            filters['targtype1_txt'] = selected_target_type

        if clickData:
            country = clickData['points'][0]['location']
            filters['country_txt'] = country

        options = get_dropdown_options('attacktype1_txt', filters)

        return options

    @app.callback(
        Output(DONUT_CHART_ID, 'figure'),
        Output(BAR_CHART_ID, 'figure'),
        Input(TARGET_TYPE_DROPDOWN_ID, 'value'),
        Input(ATTACK_TYPE_DROPDOWN_ID, 'value'),
        Input(MAP_ID, 'clickData')
    )
    
    def update_charts(selected_target_type, selected_attacks, clickData):
        filters = dict()

        if selected_target_type:
            filters['targtype1_txt'] = selected_target_type

        if clickData:
            country = clickData['points'][0]['location']
            filters['country_txt'] = country
        else:
            country = 'Global'

        donut_data = get_donut_data(selected_attacks, filters)
        bar_data = get_bar_data(selected_attacks, filters)

        donut_fig = create_donut_fig(donut_data, country)
        bar_fig = create_bar_fig(bar_data, country)

        return donut_fig, bar_fig
