from dash import Input, Output
from src.data_loader import prepare_data, calc_other_row_for_donut, filter_target_type_and_country
from src.config import FILE_PATH, TARGET_TYPE_DROPDOWN_ID, BAR_CHART_ID, DONUT_CHART_ID, MAP_ID, ATTACK_TYPE_DROPDOWN_ID
from src.data_loader import prepare_data, get_country_counts
from src.charts.map_plot import create_map
from src.charts.bar_plot import create_bar_fig
from src.charts.donut_plot import create_donut_fig


df = prepare_data(FILE_PATH)


def register_callbacks(app):
    @app.callback(
        Output(MAP_ID, 'figure'),
        Input(MAP_ID, 'clickData')
    )
    def update_map(clickData):
        highlight_country = clickData['points'][0]['location'] if clickData else None

        country_counts, labels = get_country_counts(df)

        map_fig = create_map(country_counts, labels, highlight_country)

        return map_fig

    @app.callback(
        Output(TARGET_TYPE_DROPDOWN_ID, 'options'),
        Output(TARGET_TYPE_DROPDOWN_ID, 'value'),
        Input(MAP_ID, 'clickData')
    )
    def update_target_type_dropdown(clickData):
        filtered_df = df.copy()

        if clickData:
            country = clickData['points'][0]['location']
            filtered_df = filtered_df[filtered_df['country_txt'] == country]

        return get_dropdown_options(filtered_df, 'targtype1_txt'), None

    @app.callback(
        Output(ATTACK_TYPE_DROPDOWN_ID, 'options'),
        Input(TARGET_TYPE_DROPDOWN_ID, 'value'),
        Input(MAP_ID, 'clickData')
    )
    def update_attack_type_dropdown(selected_target_type, clickData):
        filtered_df, _ = filter_target_type_and_country(
            df, selected_target_type, clickData)

        attack_type_dropdown_options = get_dropdown_options(
            filtered_df, 'attacktype1_txt')

        return attack_type_dropdown_options

    @app.callback(
        Output(DONUT_CHART_ID, 'figure'),
        Output(BAR_CHART_ID, 'figure'),
        Input(TARGET_TYPE_DROPDOWN_ID, 'value'),
        Input(ATTACK_TYPE_DROPDOWN_ID, 'value'),
        Input(MAP_ID, 'clickData')
    )
    def update_charts(selected_target_type, selected_attacks, clickData):
        filtered_df, country = filter_target_type_and_country(
            df, selected_target_type, clickData)

        if not selected_attacks:
            donut_data = filtered_df
        else:
            donut_data = filtered_df[filtered_df['attacktype1_txt'].isin(
                selected_attacks)]

        donut_data = donut_data.groupby(
            'attacktype1_txt').size().reset_index(name='count')
        donut_data = donut_data.sort_values(
            by='count', ascending=False).reset_index(drop=True)
        donut_data['percentage'] = donut_data['count'] / \
            donut_data['count'].sum()
        donut_data = calc_other_row_for_donut(donut_data, 0.05)

        bar_data = filtered_df.groupby(
            'iyear').size().reset_index(name='count')

        donut_fig = create_donut_fig(donut_data, country)
        bar_fig = create_bar_fig(bar_data, country)

        return donut_fig, bar_fig


def get_dropdown_options(filtered_df, field):
    available_types = filtered_df[field].dropna().unique()

    options = [{'label': t, 'value': t} for t in sorted(available_types)]

    return options
