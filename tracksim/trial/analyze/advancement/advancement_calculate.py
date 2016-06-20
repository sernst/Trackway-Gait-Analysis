import typing

from tracksim import events
from tracksim import limb


def strides(
        foot_positions: limb.Property,
        times: dict
) -> typing.Dict[str, list]:

    out = dict()

    for key, positions in foot_positions.items():
        distances = []
        out[key + '_strides'] = distances
        last_fixed = None

        for index, time in enumerate(times['cycles']):
            p = positions[index]

            if last_fixed is None:
                # Skip entries in motion until the first fixed position is
                # found
                if p.annotation == 'F':
                    last_fixed = p

                continue

            if p.annotation == 'F' and not last_fixed.compare(p):
                distances.append(events.Event(
                    time=time,
                    index=index,
                    value=last_fixed.distance_between(p)
                ))
                last_fixed = p

    return out
