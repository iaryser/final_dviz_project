import plotly.express as px


# Create a bar chart showing number of attacks per year
def create_bar_fig(data, country):
    """
    Creates a bar chart displaying the number of attacks per year for a given country.

    Parameters:
        data_by_year (pd.DataFrame): Must contain 'iyear' and 'count' columns.
        country_name (str): Name of the selected country (used in the chart title).

    Returns:
        plotly.graph_objects.Figure: Bar chart figure.
    """

    # Create the bar plot
    fig = px.bar(
        data,
        x='iyear',
        y='count',
        title=f"Attacks per Year in {country}",
        color_discrete_sequence=["#7e1416"]
    )

    # Customize hover tooltip
    fig.update_traces(
        hovertemplate='Year: %{label}<br>Attacks: %{value:,.0f}<extra></extra>')

    # Format chart layout and axes
    fig.update_layout(
        xaxis=dict(
            title="Year",
            dtick=10,
            tickformat='d'
        ),
        yaxis_title="Number of Attacks",
        paper_bgcolor='#3a3a3f',
        plot_bgcolor='#3a3a3f',
        font_color='white',
        title_font=dict(
            size=18,
            color='#d9d9d9',
            family='Arial, sans-serif'
        ))

    # Ensure reasonable axis range if only one year exists
    year_min = data['iyear'].min()
    year_max = data['iyear'].max()

    if year_min == year_max:
        fig.update_xaxes(range=[year_min - 1, year_max + 1])

    return fig
