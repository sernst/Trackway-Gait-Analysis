from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from tracksim import svg

def trackway_positions(limb_positions, drawer):

    bounds = [1e12, 1e12, -1e12, -1e12]
    for positions in limb_positions.values():
        for pos in positions:
            bounds[0] = min(bounds[0], pos.x.value)
            bounds[1] = min(bounds[1], pos.y.value)
            bounds[2] = max(bounds[2], pos.x.value)
            bounds[3] = max(bounds[3], pos.y.value)

    scale = 2048.0 / max(
        abs(bounds[2] - bounds[0]),
        abs(bounds[3] - bounds[1])
    )

    RADIUS = 12
    STROKE = 4

    drawer.add_style_definition('.left_pes', {
        'fill': svg.SvgWriter.LIMB_COLORS.left_pes,
        'opacity': '0.5'})
    drawer.add_style_definition('.right_pes', {
        'fill': svg.SvgWriter.LIMB_COLORS.right_pes,
        'opacity': '0.5'})
    drawer.add_style_definition('.left_manus', {
        'fill': svg.SvgWriter.LIMB_COLORS.left_manus,
        'opacity': '0.5'})

    for key, positions in limb_positions.items():
        for pos in positions:
            drawer.draw_circle(
                x=scale*pos.x.value,
                y=-scale*pos.y.value,
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
            x=scale*p0.x.value,
            y=-scale*p0.y.value,
            radius=RADIUS,
            classes=style_name,
            name=key
        )

    return {
        'scale': scale,
        'offset': (0, 0)
    }
