import pandas as pd
import plotly.graph_objects as go
from app.schemas.misc import Language
from etl.logger import get_logger
from etl.figures.utils.data_calls import (
    publication_categories
)
from etl.figures.utils.utils import plotly_fig_to_png


log = get_logger()


def generate_barchart(df: pd.DataFrame, max_graph: int, x_axis_title: str, y_axis_title: str) -> str:

    fig = go.Figure([go.Bar(
        x=df[x_axis_title],
        y=df[y_axis_title],
        width=0.3,
        marker_color='rgb(21, 96, 130)'
    )])
    fig.update_layout(
        separators=',.',
        yaxis_tickformat='.0f',
        autosize=True,
        plot_bgcolor="rgb(229, 241, 249)",
        paper_bgcolor="rgb(229, 241, 249)",
        margin=dict(l=20, r=20, t=20, b=20),
        width=1300,
        height=350,
        yaxis=dict(range=[0, max_graph]) 
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='rgba(21, 66, 115, 0.5)', title=x_axis_title)
    fig.update_yaxes(showline=False, gridcolor='rgba(21, 66, 115, 0.5)', title=y_axis_title)
    
    return plotly_fig_to_png(fig)


def generate_barchart_publication_categories(lang: Language, x_axis_title: str, y_axis_title: str) -> str:
    log.info(f"Generating barchart for {lang} publication categories")
    df, max_graph = publication_categories(lang, x_axis_title, y_axis_title)
    return generate_barchart(df, max_graph, x_axis_title, y_axis_title)
