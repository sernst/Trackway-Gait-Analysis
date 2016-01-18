
from tracksim import svg
from tracksim import trackway

def trackway_positions(limb_positions, drawer):

    max_x = -1e12
    max_y = -1e12

    for positions in limb_positions.values():
        for pos in positions:
            max_x = max(max_x, pos.x.value)
            max_y = max(max_y, pos.y.value)

    drawer.scale = 1280.0 / max_x
    origin = trackway.TrackPosition.from_raw_values(
        x=0, x_uncertainty=0,
        y=max_y, y_uncertainty=0)

    drawer.set_offset(y=max_y)

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
        track_positions(
            positions=positions,
            drawer=drawer,
            classes=key,
            origin=origin,
            scale=drawer.scale)

def track_positions(positions, drawer, classes, origin, scale = 1.0):

    for pos in positions:
        drawer.draw_circle(
            x=scale*(pos.x + origin.x).value,
            y=scale*(pos.y + origin.y).value,
            radius=10,
            classes=classes)
