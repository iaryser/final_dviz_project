import plotly.express as px


def create_donut_fig(data, country):
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

    # PIE: Different attack types
    fig = px.pie(
        data,
        names='attacktype1_txt',
        values='count',
        title=f"Attack Types in {country}",
        color_discrete_sequence=serious_palette,
        hole=0.5
    )

    fig.update_traces(
        hovertemplate='%{label}<br>%{value:,.0f}<extra></extra>',
        direction='clockwise'
    )

    # black background
    fig.update_layout(
        paper_bgcolor='#3a3a3f',
        plot_bgcolor='#3a3a3f',
        font_color='white',
        title_font=dict(
            size=18,
            color='#d9d9d9',
            family='Arial, sans-serif'
        ))

    fig.update_layout(
        legend_itemclick=False,
        legend_itemdoubleclick=False
    )

    return fig
