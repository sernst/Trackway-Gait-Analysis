import pandas as pd
from plotly import graph_objs as go


def create(
        df: pd.DataFrame,
        values,
        x_values=None
):
    """

    :param df:
    :param values:
    :param x_values:
    :return:
    """

    traces = []

    df = df.copy()  # type: pd.DataFrame

    if isinstance(values, str):
        df['y'] = df[values].tolist()
    else:
        try:
            df['y'] = values.tolist()
        except Exception:
            df['y'] = values

    if x_values is None:
        df['x'] = df.coupling_length.tolist()
    elif isinstance(x_values, str):
        df['x'] = df[x_values].tolist()
    else:
        try:
            df['x'] = x_values.tolist()
        except Exception:
            df['x'] = x_values

    for gait_id in df.gait_id.unique():
        df_slice = df[df.gait_id == gait_id]

        for index, row in df_slice.iterrows():
            traces.append(go.Scatter(
                x=[row.x, row.x],
                y=[0, row.y],
                mode='lines',
                hoverinfo='none',
                line=dict(
                    color=row.color,
                    width=2
                ),
                legendgroup=gait_id,
                showlegend=False
            ))

        traces.append(go.Scatter(
            x=df_slice.x,
            y=df_slice.y,
            text=df_slice.short_id,
            name=gait_id,
            mode='markers',
            marker=dict(
                color=df_slice.color,
                size=10
            ),
            legendgroup=gait_id
        ))

    return traces


