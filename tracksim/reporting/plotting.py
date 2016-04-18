import typing

PLOT_COLOR_PALETTE = (
    (31, 119, 180),
    (255, 127, 14),
    (44, 160, 44),
    (214, 39, 40),
    (148, 103, 189),
    (140, 86, 75),
    (227, 119, 194),
    (127, 127, 127),
    (188, 189, 34),
    (23, 190, 207)
)


def get_color(
        index: int,
        opacity:float = None,
        as_string: bool = False
) -> typing.Union[tuple, str]:

    out = PLOT_COLOR_PALETTE[index % len(PLOT_COLOR_PALETTE)]

    if opacity is None:
        opacity = 1.0

    out = tuple(list(out) + [opacity])
    if as_string:
            return 'rgba({}, {}, {}, {})'.format(*out)

    return out


def create_layout(
        layout: dict = None,
        title: str = None,
        x_label: str = None,
        y_label: str = None
) -> dict:
    """

    :param layout:
    :param title:
    :param x_label:
    :param y_label:
    :return:
    """

    if layout is None:
        layout = dict()

    layout['title'] = title if title else layout.get('title')

    font = {
        'family': 'Courier New, monospace',
        'size': 18,
        'color': '#7f7f7f'
    }

    x = layout.get('xaxis', {})
    x['title'] = x_label if x_label else x['title']
    x['titlefont'] = x.get('titlefont', font)
    layout['xaxis'] = x

    y= layout.get('yaxis', {})
    y['title'] = y_label if y_label else y['title']
    y['titlefont'] = y.get('titlefont', font)
    layout['yaxis'] = y

    return layout


def make_line_data(x: list, y: list, y_unc: list):

    lower = []
    upper = []

    for y_value, y_unc_value in zip(y, y_unc):
        lower.append(y_value - y_unc_value)
        upper.append(y_value + y_unc_value)


    lowerTrace = dict(
        x=x,
        y=lower,
        line={'width': 0},
        marker={'color': '444'},
        mode='lines',
        name='Lower Bound',
        type='scatter'
    )

    middleTrace = dict(
        x=x,
        y=y,
        fill='tonexty',
        fillcolor='rgba(68, 68, 68, 0.1)',
        line={'color': 'rgb(31, 119, 180)'},
        mode='markers',
        name='Measurement',
        type='scatter'
    )

    upperTrace = dict(
        x=x,
        y=upper,
        fill='tonexty',
        fillcolor='rgba(68, 68, 68, 0.1)',
        line={'width': 0},
        marker={'color': '444'},
        mode='lines',
        name='Upper Bound',
        type='scatter'
    )

    return {
        'data': [lowerTrace, middleTrace, upperTrace],
        'layout': {'showlegend': False}
    }


