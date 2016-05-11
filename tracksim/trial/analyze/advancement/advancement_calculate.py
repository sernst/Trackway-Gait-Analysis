import typing

import measurement_stats as mstats

from tracksim import limb


def strides(
        foot_positions: limb.Property
) -> typing.Dict[str, list]:

    out = dict()

    for key, positions in foot_positions.items():

        distances = []
        out[key + '_strides'] = distances

        last_fixed = None
        for p in positions:
            if last_fixed is None:
                # Skip entries in motion until the first fixed position is
                # found

                distances.append(mstats.ValueUncertainty(0, 0.0001))
                if p.annotation == 'F':
                    last_fixed = p

                continue

            if p.annotation == 'F':

                if last_fixed.compare(p):
                    distances.append(distances[-1].clone())
                else:
                    distances.append(last_fixed.distance_between(p))
                    last_fixed = p
            else:
                distances.append(last_fixed.distance_between(p))

    return out
