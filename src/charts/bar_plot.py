import plotly.express as px


def create_bar_fig(data, country):
    # BAR: Number of attacks per year
    fig = px.bar(
        data,
        x='iyear',
        y='count',
        title=f"Attacks per Year in {country}",
        color_discrete_sequence=["#7e1416"]
    )

    fig.update_traces(
        hovertemplate='Year: %{label}<br>Attacks: %{value:,.0f}<extra></extra>')

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

    year_min = data['iyear'].min()
    year_max = data['iyear'].max()

    if year_min == year_max:
        year_min -= 1
        year_max += 1
        fig.update_xaxes(range=[year_min, year_max])

    return fig
