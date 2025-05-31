import plotly.express as px


# Create a donut chart showing distribution of attack types
def create_donut_fig(data, country):
    """
    Generates a donut chart displaying the distribution of attack types
    for a given country or globally.

    Parameters:
        attack_summary_df (pd.DataFrame): Must contain 'attacktype1_txt' and 'count'.
        country_name (str): Country name to display in the title.

    Returns:
        plotly.graph_objects.Figure: Donut chart figure.
    """

    serious_palette = [
        "#8c1515",  # deep red (danger)
        "#b33636",  # brick
        "#d66c6c",  # clay
        "#5c5c5c",  # gunmetal
        "#3c6e71",  # desaturated blue-green
        "#556c8d",  # military navy
        "#8a8780",  # grey-brown
        "#947c67",  # sand/military tan
        "#8f3b76",  # muted wine
        "#4e4c67"   # steel purple
    ]

    # Build donut chart
    fig = px.pie(
        data,
        names='attacktype1_txt',
        values='count',
        title=f"Attack Types in {country}",
        color_discrete_sequence=serious_palette,
        hole=0.5
    )

    # Customize hover tooltip and draw clockwise
    fig.update_traces(
        hovertemplate='%{label}<br>%{value:,.0f}<extra></extra>',
        direction='clockwise'
    )

    # Dark theme styling
    fig.update_layout(
        paper_bgcolor='#3a3a3f',
        plot_bgcolor='#3a3a3f',
        font_color='white',
        title_font=dict(
            size=18,
            color='#d9d9d9',
            family='Arial, sans-serif'
        ))

    # Disable click filtering from the legend
    fig.update_layout(
        legend_itemclick=False,
        legend_itemdoubleclick=False
    )

    return fig
