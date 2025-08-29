import pandas as pd
import plotly.express as px
from app.schemas.misc import Language
from etl.logger import get_logger
from etl.figures.utils.data_calls import (
    published_algorithmdescriptions_permonth,
    organisations_permonth,
    broken_links_perday
)
from etl.figures.utils.utils import plotly_fig_to_png


log = get_logger(__name__)


# Generates a linechart gif image
def generate_linechart(df: pd.DataFrame, max_graph: int, x_axis_title: str, y_axis_title: str, broken_link_chart=False) -> str:

    if(broken_link_chart):
        x_tick_format="%d-%m"
        fig_height = 350
        x_type = 'category'
    else:
        df.index = pd.to_datetime(df.index, format="%d-%m-%Y")
        x_tick_format="%m-%Y"
        fig_height = 600
        x_type = 'date'

    # make the fig
    fig = px.line(df, x=df.index, y=df["aantal"], color_discrete_sequence=['rgb(21, 96, 130)'])
    fig.update_layout(
        xaxis_title=x_axis_title,
        yaxis_range=[0, max_graph + 1],
        yaxis_title=y_axis_title,
        plot_bgcolor="rgb(229, 241, 249)",
        paper_bgcolor="rgb(229, 241, 249)",
        margin=dict(l=20, r=20, t=20, b=20),
        width=1300,
        height=fig_height,
    )

    fig.update_xaxes(
        tickformat=x_tick_format,
        type=x_type,
        showline=True,
        linecolor="rgba(21, 66, 115, 0.5)",
        showgrid=False,
        dtick="M1",
        title_font=dict(family="Arial Black, sans-serif"),
        tickfont=dict(color="grey"),
    )
    fig.update_yaxes(
        showline=False,
        gridcolor="rgba(21, 66, 115, 0.5)",
        title_font=dict(family="Arial Black, sans-serif"),
        tickfont=dict(color="grey"),
    )

    return plotly_fig_to_png(fig)


def generate_linechart_joined_organisations_permonth(lang: Language, x_axis_title: str, y_axis_title: str) -> str:
    log.info(f"Generating animated chart for {lang} joined organisations per month")
    df, max_graph = organisations_permonth()
    return generate_linechart(df, max_graph, x_axis_title, y_axis_title)


def generate_linechart_published_algorithmdescriptions_permonth(lang: Language, x_axis_title: str, y_axis_title: str) -> str:
    log.info(f"Generating animated chart for {lang} algorithm descriptions per month")
    df, max_graph = published_algorithmdescriptions_permonth()
    return generate_linechart(df, max_graph, x_axis_title, y_axis_title)


def generate_linechart_broken_links_perday(lang: Language, x_axis_title: str, y_axis_title: str) -> str:
    log.info(f"Generating animated chart for {lang} broken links per day")
    df, max_graph= broken_links_perday(lang)
    return generate_linechart(df, max_graph, x_axis_title, y_axis_title, broken_link_chart=True)
