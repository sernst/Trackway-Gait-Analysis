from tracksim import limb
from tracksim import svg

RADIUS = 12
STROKE = 4


def trackway_positions(limb_positions, drawer, positions=None):
    """
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
        'opacity': '0.5'})
    drawer.add_style_definition('.right_pes', {
        'fill': svg.SvgWriter.LIMB_COLORS.right_pes,
        'opacity': '0.5'})
    drawer.add_style_definition('.left_manus', {
        'fill': svg.SvgWriter.LIMB_COLORS.left_manus,
        'opacity': '0.5'})
    drawer.add_style_definition('.right_manus', {
        'fill': svg.SvgWriter.LIMB_COLORS.right_manus,
        'opacity': '0.5'})

    for key, positions in limb_positions.items():
        for pos in positions:
            drawer.draw_circle(
                x=scale*pos.x.raw,
                y=-scale*pos.y.raw,
                radius=RADIUS,
                classes=key)

        drawer.add_style_definition('.{}'.format(key), {
            'fill': svg.SvgWriter.LIMB_COLORS.get(key),
            'opacity': '0.5'
        })

        style_name = '{}-marker'.format(key)
        style = {
            'fill': 'transparent',
            'stroke-width': '{}px'.format(STROKE),
            'stroke': svg.SvgWriter.LIMB_COLORS.get(key)
        }

        if key.find('manus') != -1:
            style['stroke-dasharray'] = '{},{}'.format(STROKE, STROKE)

        drawer.add_style_definition('.{}'.format(style_name), style)

        p0 = positions[0]
        drawer.draw_circle(
            x=scale*p0.x.raw,
            y=-scale*p0.y.raw,
            radius=RADIUS,
            classes=style_name,
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
