from scipy import stats
import plotly.express as px


def stats_label(x, y):
    list_x = list(x)
    list_y = list(y)
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        list_x, list_y
    )
    stats_label = f"y = {round(intercept, 4)} + {round(slope, 4)}x<br>R<sup>2</sup> = {round((r_value ** 2), 4)}"
    return stats_label


def show_graph(data):
    label = stats_label(data["Plink_F_value"], data["Freq_rsIDs_F_value"])
    fig = px.scatter(
        data,
        x="Plink_F_value",
        y="Freq_rsIDs_F_value",
        trendline="ols",
        trendline_color_override="#440154",
        template="plotly_white"
    )
    fig.update_traces(marker_size=2, marker=dict(color="#4682b4"))
    fig.add_annotation(
        text=label,
        showarrow=False,
        xref="paper",
        yref="paper",
        x=0.05,
        y=0.95,
        font=dict(
            weight="bold",
            size=20
        )
    )
    fig.update_xaxes(
        ticks='outside',
        showline=True,
        linewidth=2, 
        linecolor='black'
    )
    fig.update_yaxes(
        ticks='outside',
        showline=True,
        linewidth=2, 
        linecolor='black'
    )
    return fig
