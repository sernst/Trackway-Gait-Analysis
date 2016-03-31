from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from datetime import datetime

import measurement_stats as mstats

import tracksim
from tracksim import limb
from tracksim import reporting
from tracksim import svg
from tracksim.svg import draw


def create(trial_configs, track_definition, results):
    """

    :param trial_configs:
    :param track_definition:
    :param results:
    :return:
    """

    sim_id = trial_configs['name'].replace(' ', '-')
    output_directory = tracksim.make_results_path('report', 'trials', sim_id)

    drawer = svg.SvgWriter(padding=5)
    svg_settings = draw.trackway_positions(
        limb_positions=track_definition.limb_positions,
        positions=results['positions'],
        drawer=drawer
    )

    cycles = make_cycle_data(drawer, results)

    data = {
        'id': sim_id,
        'configs': trial_configs,
        'date': datetime.utcnow().strftime("%m-%d-%Y %H:%M"),
        'scale': svg_settings['scale'],
        'offset': svg_settings['offset'],
        'markerIds': limb.KEYS + [],
        'cycles': cycles.toDict(),
        'couplings': make_formatted_coupling_data(results),
        'separations': make_formatted_separation_data(results),
        'extensions': make_formatted_extension_data(results),
        'frames': make_animation_frame_data(drawer, results),
        'time': make_time_data(results),
        'limb_phases': track_definition.limb_phases.toDict(),
        'svg': drawer.dumps()
    }

    reporting.write_javascript_files(
        directory=output_directory,
        sim_id=sim_id,
        key='SIM_DATA',
        data=data
    )

    svg_path = os.path.join(output_directory, '{}.svg'.format(sim_id))
    drawer.write(svg_path)

    return data

def create_file_from_template(src_path, dest_path, replacements):
    """

    :param src_path:
    :param dest_path:
    :param replacements:
    :return:
    """

    with open(src_path, 'r+') as f:
        contents = f.read()

    for key, value in replacements.items():
        contents = contents.replace(key, value)

    with open(dest_path, 'w+') as f:
        f.write(contents)

    return dest_path

def make_animation_frame_data(drawer, results):
    """

    :param drawer:
    :param results:
    :return:
    """

    positions = results['positions']
    steps = len(results['times'])
    frames = []

    for i in range(steps):
        frames.append({'time':results['times'][i], 'positions':[]})
        for key in limb.KEYS:
            pos = positions.get(key)[i]
            frames[-1]['positions'].append({
                'x':[pos.x.value, pos.x.uncertainty],
                'y':[pos.y.value, pos.y.uncertainty],
                'f': pos.annotation
            })

    return frames

def make_cycle_data(drawer, results):
    """

    :param drawer:
    :param results:
    :return:
    """

    gait_cycles = limb.Property().assign([], [], [], [])
    positions = results['positions']
    steps = len(results['times'])

    for i in range(steps):
        for key in limb.KEYS:
            cycles = gait_cycles.get(key)
            pos = positions.get(key)[i]
            if not cycles or cycles[-1][1] != pos.annotation:
                cycles.append([1, pos.annotation])
            else:
                cycles[-1][0] += 1

    return gait_cycles

def make_formatted_coupling_data(results):
    """

    :param results:
    :return:
    """

    data = results['couplings']
    vals, uncs = mstats.values.unzip(data['data'])

    return dict(
        values=vals,
        uncertainties=uncs,
        deviation_max=data['deviation_max'],
        result=data['value'].html_label,
        bounds=data['bounds']
    )

def make_formatted_separation_data(results):
    """

    :param results:
    :return:
    """

    out = {}
    for key in ['left', 'right', 'front', 'back']:
        data = results['separations'][key]
        values = []
        uncertainties = []

        for v in data:
            values.append(v.value)
            uncertainties.append(v.uncertainty)

        mean = mstats.mean.weighted_mean_and_deviation(*data)
        deviations = mstats.values.deviations(mean.value, data)

        out[key] = dict(
            values=values,
            deviation_max=mstats.value.round_to_order(max(deviations), -2),
            uncertainties=uncertainties,
            result=mean.html_label,
            value=[mean.value, mean.uncertainty]
        )

    return out

def make_formatted_extension_data(results):
    """

    :param results:
    :return:
    """

    out = {}
    for key in limb.KEYS:
        data = results['extensions'].get(key)
        values = []
        uncertainties = []

        for v in data:
            values.append(v.value)
            uncertainties.append(v.uncertainty)

        mean = mstats.mean.weighted_mean_and_deviation(*data)
        deviations = mstats.values.deviations(mean.value, data)

        out[key] = dict(
            values=values,
            deviation_max=mstats.value.round_to_order(max(deviations), -2),
            uncertainties=uncertainties,
            result=mean.html_label,
            value=[mean.value, mean.uncertainty]
        )

    return out

def make_time_data(results):
    """

    :param results:
    :return:
    """

    count = len(results['times'])
    times = list(results['times'])
    progress = list(mstats.ops.linear_space(0, 100.0, count))

    return {
        'count': count,
        'cycles': times,
        'progress': progress
    }

