from dash import Input, Output, State, callback_context
from dash.exceptions import PreventUpdate

from src.data_loader import (
    get_filter_options,
    get_map_data,
    get_donut_data,
    get_bar_data
)

from src.config import (
    TARGET_TYPE_DROPDOWN_ID,
    BAR_CHART_ID,
    DONUT_CHART_ID,
    MAP_ID,
    ATTACK_TYPE_DROPDOWN_ID,
    SELECTED_COUNTRY_STORE,
    COUNTRY_RESET_BUTTON_ID
)

from src.charts.map_plot import create_map
from src.charts.bar_plot import create_bar_fig
from src.charts.donut_plot import create_donut_fig


# Register all app interactivity
def register_callbacks(app):

    # Update the world map whenever a new country is selected
    @app.callback(
        Output(MAP_ID, 'figure'),
        Input(SELECTED_COUNTRY_STORE, 'data')
    )
    def update_map(selected_country):
        country_counts, labels = get_map_data()
        return create_map(country_counts, labels, selected_country)

    # Handle country selection from map clicks or reset button
    @app.callback(
        Output(SELECTED_COUNTRY_STORE, 'data'),
        Input(MAP_ID, 'clickData'),
        Input(COUNTRY_RESET_BUTTON_ID, 'n_clicks'),
        State(SELECTED_COUNTRY_STORE, 'data')
    )
    def update_selected_country(clickData, n_clicks, selected_country):
        triggered_id = callback_context.triggered_id

        # If reset button was clicked, clear selection
        if triggered_id == COUNTRY_RESET_BUTTON_ID:
            if n_clicks:
                return None
            raise PreventUpdate

        # If map was clicked, update to clicked country
        if triggered_id == MAP_ID and clickData and 'points' in clickData:
            clicked_country = clickData['points'][0]['location']
            return None if clicked_country == selected_country else clicked_country

        raise PreventUpdate

    # Populate the "Target Type" dropdown based on selected country
    @app.callback(
        Output(TARGET_TYPE_DROPDOWN_ID, 'options'),
        Output(TARGET_TYPE_DROPDOWN_ID, 'value'),
        Input(SELECTED_COUNTRY_STORE, 'data')
    )
    def update_target_type_dropdown(selected_country):
        if selected_country:
            options = get_filter_options(
                'targtype1_txt', {'country_txt': selected_country}
            )
        else:
            options = get_filter_options('targtype1_txt')

        return options, None  # reset value after country change

    # Populate "Attack Types" based on target type and selected country
    @app.callback(
        Output(ATTACK_TYPE_DROPDOWN_ID, 'options'),
        Input(TARGET_TYPE_DROPDOWN_ID, 'value'),
        Input(SELECTED_COUNTRY_STORE, 'data')
    )
    def update_attack_type_select(selected_target_type, selected_country):
        filters = {}

        if selected_target_type:
            filters['targtype1_txt'] = selected_target_type

        if selected_country:
            filters['country_txt'] = selected_country

        options = get_filter_options('attacktype1_txt', filters)
        return options

    # Update donut and bar charts based on filters and selected attacks
    @app.callback(
    Output(DONUT_CHART_ID, 'figure'),
    Output(BAR_CHART_ID, 'figure'),
    Input(TARGET_TYPE_DROPDOWN_ID, 'value'),
    Input(ATTACK_TYPE_DROPDOWN_ID, 'value'),
    Input(SELECTED_COUNTRY_STORE, 'data')
    )
    def update_charts(selected_target_type, selected_attacks, selected_country):
        filters = {}

        # Apply filters based on current UI selections
        if selected_target_type:
            filters['targtype1_txt'] = selected_target_type
        if selected_country and selected_country != 'Global':
            filters['country_txt'] = selected_country

        # Get pre-processed data from loader
        donut_data = get_donut_data(selected_attacks, filters)
        bar_data = get_bar_data(selected_attacks, filters)

        # Use "Global" if no country is selected
        location_label = selected_country or 'Global'

        # Create both visualizations
        donut_fig = create_donut_fig(donut_data, location_label)
        bar_fig = create_bar_fig(bar_data, location_label)

        return donut_fig, bar_fig
