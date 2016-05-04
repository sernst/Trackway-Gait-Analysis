from tracksim import limb
from tracksim import svg

PES_RADIUS = 12
RADIUS = 8
STROKE = 8


def trackway_positions(
        limb_positions: limb.Property,
        drawer,
        positions=None
):
    """

    :param limb_positions:
    :param drawer:
    :param positions:
    :return:
    """

    limb_positions = create_positions(limb_positions, positions)

    bounds = [1e12, 1e12, -1e12, -1e12]
    for positions in limb_positions.values():
        for pos in positions:
            bounds[0] = min(bounds[0], pos.x.raw, pos.x.value)
            bounds[1] = min(bounds[1], pos.y.raw, pos.y.value)
            bounds[2] = max(bounds[2], pos.x.raw, pos.x.value)
            bounds[3] = max(bounds[3], pos.y.raw, pos.y.value)

    scale = 2048.0 / max(
        abs(bounds[2] - bounds[0]),
        abs(bounds[3] - bounds[1])
    )

    drawer.add_style_definition('.left_pes', {
        'fill': svg.SvgWriter.LIMB_COLORS.left_pes,
        'opacity': '0.5'
    })

    drawer.add_style_definition('.right_pes', {
        'fill': svg.SvgWriter.LIMB_COLORS.right_pes,
        'opacity': '0.5'
    })

    drawer.add_style_definition('.left_manus', {
        'fill': svg.SvgWriter.LIMB_COLORS.left_manus,
        'opacity': '0.5'
    })

    drawer.add_style_definition('.right_manus', {
        'fill': svg.SvgWriter.LIMB_COLORS.right_manus,
        'opacity': '0.5'
    })

    for key, positions in limb_positions.items():
        is_pes = key in [limb.LEFT_PES, limb.RIGHT_PES]

        for pos in positions:
            classes = [key, 'track-pos']

            html_data = {
                'x': '{}'.format(pos.x.value),
                'x-unc': '{}'.format(pos.x.uncertainty),
                'y': '{}'.format(pos.y.value),
                'y-unc': '{}'.format(pos.y.uncertainty),
                'color': svg.SvgWriter.LIMB_COLORS.get(key)
            }

            if pos.annotation:
                html_data['annotation'] = pos.annotation
            if pos.uid:
                html_data['uid'] = pos.uid
            if pos.name:
                html_data['name'] = pos.name
            if pos.assumed:
                html_data['assumed'] = '1'
                classes.append('assumed')

            drawer.draw_circle(
                x=scale*pos.x.raw,
                y=-scale*pos.y.raw,
                radius=PES_RADIUS if is_pes else RADIUS,
                classes=classes,
                data=html_data
            )

        color = svg.SvgWriter.LIMB_COLORS.get(key)

        print_style_name = '.{}'.format(key)
        print_style = {
            'fill': color,
            'opacity': '0.5',
            'stroke-width': '{}px'.format(STROKE),
            'stroke': color
        }

        assumed_style_name = '.{}.assumed'.format(key)
        assumed_style = {
            'fill': 'white',
            'opacity': '0.33'
        }

        marker_style_name = '.{}-marker'.format(key)
        marker_style = {
            'fill': 'transparent',
            'stroke-width': '{}px'.format(STROKE),
            'stroke': color
        }

        if not is_pes:
            dash_array = '{},{}'.format(4, 4)
            marker_style['stroke-dasharray'] = '{},{}'.format(8,4)
            print_style['stroke-dasharray'] = dash_array
            assumed_style['stroke-dasharray'] = dash_array

        drawer.add_style_definition(print_style_name, print_style)
        drawer.add_style_definition(assumed_style_name, assumed_style)
        drawer.add_style_definition(marker_style_name, marker_style)

        p0 = positions[0]
        drawer.draw_circle(
            x=scale*p0.x.raw,
            y=-scale*p0.y.raw,
            radius=(PES_RADIUS if is_pes else RADIUS) + 0.5 * STROKE,
            classes=marker_style_name[1:],
            name=key
        )

    return {
        'scale': scale,
        'offset': (0, 0)
    }


def create_positions(limb_positions, foot_positions):
    """
    """

    if not foot_positions:
        return limb_positions

    out = limb.Property()

    for key in limb.KEYS:
        positions = foot_positions.get(key)
        track_positions = []
        started_fixed = positions[0].annotation == 'F'

        for p in positions:
            if p.annotation != 'F':
                continue
            elif track_positions and p.compare(track_positions[-1]):
                continue

            track_positions.append(p)

        if not started_fixed:
            # If the simulation started with this limb in motion, find the
            # previous limb position and add that to the list to serve as a
            # reference point in the drawing (if such a previous track exists).
            prev = None
            for lp in limb_positions.get(key):
                if lp.compare(track_positions[0]):
                    if prev:
                        track_positions.insert(0, prev)
                    break
                prev = lp

        out.set(key, track_positions)

    return out
