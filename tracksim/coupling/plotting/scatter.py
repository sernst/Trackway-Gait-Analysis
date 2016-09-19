import typing
import pandas as pd
import plotly.graph_objs as go
from tracksim.coupling.plotting import styles
import numpy as np


def slice_column(df: pd.DataFrame, column: typing.Union[str, list] = None):
    """

    :param df:
    :param column:
    :return:
    """

    if isinstance(column, str):
        return df[column]
    elif column is None:
        return None

    if isinstance(column, pd.Series):
        return [column.iloc[pos] for pos in df['__position__']]

    return [column[pos] for pos in df['__position__']]


def make_trace(
        name: str,
        color: typing.Union[str, int],
        value_column: typing.Union[pd.Series, list],
        uncertainty_column: typing.Union[pd.Series, list] = None,
        x_column: typing.Union[pd.Series, list] = None,
        text_column: typing.Union[pd.Series, list] = None
):
    """

    :param name:
    :param color:
    :param value_column:
    :param uncertainty_column:
    :param x_column:
    :param text_column:
    :return:
    """

    if uncertainty_column is not None:
        error_y = dict(
            type='data',
            visible=True,
            array=uncertainty_column
        )
    else:
        error_y = {'visible': False}

    return go.Scatter(
        x=x_column,
        y=value_column,
        error_y=error_y,
        mode='markers',
        marker={'size': 6, 'color': color},
        text=text_column,
        name=name
    )


def create(
        data_frame: pd.DataFrame,
        value_column: typing.Union[str, list],
        uncertainty_column: typing.Union[str, list] = None,
        x_column: typing.Union[str, list] = None,
        sort_by: typing.Union[str, list] = 'separation'
):
    """
    Create a scatter plot for each row in the specified data frame where the
    x, y and y uncertainty values are defined by column names or a Series/list
    where the elements match the order of the entries in the data frame.

    :param data_frame:
    :param value_column:
    :param uncertainty_column:
    :param x_column:
    :param sort_by:
    :return:
    """

    traces = []
    data_frame = data_frame.copy()  # type: pd.DataFrame
    df = data_frame.copy()  # type: pd.DataFrame

    df['__position__'] = np.arange(0, df.shape[0], 1)

    for index, gait_id in enumerate(sorted(data_frame.gait_id.unique())):
        df_slice = df[df['gait_id'] == gait_id]

        if sort_by is not None:
            df_slice = df_slice.sort_values(by=sort_by)

        traces.append(make_trace(
            name=gait_id,
            color=styles.GAIT_COLORS[index],
            value_column=slice_column(df_slice, value_column),
            uncertainty_column=slice_column(df_slice, uncertainty_column),
            x_column=slice_column(df_slice, x_column),
            text_column=df_slice['short_id']
        ))

    return traces
