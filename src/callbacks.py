from dash import Input, Output, State, callback_context
from dash.exceptions import PreventUpdate
from src.data_loader import get_dropdown_options, get_map_data, get_donut_data, get_bar_data
from src.config import TARGET_TYPE_DROPDOWN_ID, BAR_CHART_ID, DONUT_CHART_ID, MAP_ID, ATTACK_TYPE_DROPDOWN_ID, SELECTED_COUNTRY_STORE, COUNTRY_RESET_BUTTON_ID
from src.charts.map_plot import create_map
from src.charts.bar_plot import create_bar_fig
from src.charts.donut_plot import create_donut_fig


def register_callbacks(app):
    @app.callback(
        Output(MAP_ID, 'figure'),
        Input(SELECTED_COUNTRY_STORE, 'data')
    )
    def update_map(selected_country):
        country_counts, labels = get_map_data()
        return create_map(country_counts, labels, selected_country)

    @app.callback(
        Output(SELECTED_COUNTRY_STORE, 'data'),
        Input(MAP_ID, 'clickData'),
        Input(COUNTRY_RESET_BUTTON_ID, 'n_clicks'),
        State(SELECTED_COUNTRY_STORE, 'data')
    )
    def update_selected_country(clickData, n_clicks, selected_country):
        triggered_id = callback_context.triggered_id

        if triggered_id == COUNTRY_RESET_BUTTON_ID:
            if n_clicks:
                return None
            raise PreventUpdate

        if triggered_id == MAP_ID and clickData and 'points' in clickData:
            clicked_country = clickData['points'][0]['location']
            return None if clicked_country == selected_country else clicked_country

        raise PreventUpdate

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
    Input(SELECTED_COUNTRY_STORE, 'data')
)
    def update_charts(selected_target_type, selected_attacks, selected_country):
        filters = {}

        if selected_target_type:
            filters['targtype1_txt'] = selected_target_type
        if selected_country and selected_country != 'Global':
            filters['country_txt'] = selected_country

        donut_data = get_donut_data(selected_attacks, filters)
        bar_data = get_bar_data(selected_attacks, filters)

        donut_fig = create_donut_fig(donut_data, selected_country or 'Global')
        bar_fig = create_bar_fig(bar_data, selected_country or 'Global')

        return donut_fig, bar_fig
