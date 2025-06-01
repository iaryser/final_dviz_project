import plotly.express as px


# Create a choropleth map showing attack intensity by country
def create_map(country_counts, labels, highlight_country=None):
    """
    Creates a choropleth map visualizing attack frequency per country,
    categorized by attacks per million inhabitants.

    Parameters:
        country_df (pd.DataFrame): Must contain 'country_txt', 'attack_bin', and 'attack_count'.
        attack_bins (list): Ordered list of bin labels for coloring.
        highlight_country (str, optional): If provided, outline this country on the map.

    Returns:
        plotly.graph_objects.Figure: Choropleth map.
    """

    # Define a custom discrete color scale matching attack bins
    hex_colors = ["#d9d9d9", "#f4a6a6", "#e06666",
                  "#cc3c3c", "#a31515", "#7e1416"]
    color_map = dict(zip(labels, hex_colors))

    # Map projection settings
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

    # Customize color legend
    fig.update_coloraxes(colorbar_title="Number of Attacks")

    # Geo-Settings
    fig.update_geos(
        projection_type="natural earth",
        projection_scale=1.2,
        center={"lat": 20, "lon": 0},
        showcountries=True,
        bgcolor='#3a3a3f',
        showframe=True,
        showcoastlines=True
    )

    # Customize hover appearance
    fig.update_traces(
        hovertemplate=(
            "<b>%{location}</b><br>"
            "Attacks: %{customdata[0]:,}<br>"
            "<extra></extra>"
        )
    )

    # Apply dark theme and layout styling
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        autosize=True,
        paper_bgcolor='#3a3a3f',
        plot_bgcolor='#3a3a3f',
        font_color='#d9d9d9',
        hoverlabel=dict(
            bgcolor="rgba(50,50,50,0.8)",
            font_size=13,
            font_family="Arial, sans-serif",
            font_color="#d9d9d9",
            bordercolor="#666"
        ),
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

    # Highlight selected country with a golden border
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
