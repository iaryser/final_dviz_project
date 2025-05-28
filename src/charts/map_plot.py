import plotly.express as px


def create_map(country_counts, labels, highlight_country=None):
    # map each label to desired colorscale
    hex_colors = ["#d9d9d9", "#f4a6a6", "#e06666",
                  "#cc3c3c", "#a31515", "#7e1416"]
    color_map = dict(zip(labels, hex_colors))
    fig = px.choropleth(
        country_counts,
        locations="country_txt",
        locationmode="country names",
        color="attack_bin",
        color_discrete_map=color_map,
        category_orders={'attack_bin': labels},
        labels={'attack_bin': 'Attack Range'},
        custom_data=['attack_count']
    )

    fig.update_coloraxes(colorbar_title="Number of Attacks")

    # Geo-Settings
    fig.update_geos(
        showframe=True,
        showcoastlines=True
    )

    # Dark Design & Tooltyp styling
    fig.update_traces(
        hovertemplate=(
            "<b>%{location}</b><br>"
            "Attacks: %{customdata[0]:,}<br>"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        geo=dict(
            projection_type="natural earth",
            projection_scale=1.2,
            center={"lat": 20, "lon": 0},
            showcountries=True,
            bgcolor='#3a3a3f'
        ),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        autosize=True,
        hoverlabel=dict(
            bgcolor="rgba(50,50,50,0.8)",
            font_size=13,
            font_family="Arial, sans-serif",
            font_color="#d9d9d9",
            bordercolor="#666"
        ),
        paper_bgcolor='#3a3a3f',
        plot_bgcolor='#3a3a3f',
        font_color='#d9d9d9'
    )

    fig.update_layout(
        legend=dict(
            title=dict(text="Attacks per Million", font=dict(size=18)),
            font=dict(size=14),
            itemwidth=50,
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )

    if highlight_country:
        fig.add_choropleth(
            locations=[highlight_country],
            locationmode="country names",
            z=[1],
            colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],
            showscale=False,
            hoverinfo='skip',
            marker=dict(
                line=dict(
                    color='gold',
                    width=3
                )
            )
        )

    return fig
