import plotly.express as px


def create_donut_fig(data, country):
    # PIE: Different attack types
    fig = px.pie(
        data,
        names='attacktype1_txt',
        values='count',
        title=f"Attack Types in {country}",
        color_discrete_sequence=px.colors.sequential.Reds[::-1],
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
