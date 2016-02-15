
import os
import shutil
import json
from json import encoder
from datetime import datetime

import tracksim
from tracksim import number
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

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    drawer = svg.SvgWriter(padding=5)
    svg_settings = draw.trackway_positions(
        limb_positions=track_definition.limb_positions,
        drawer=drawer
    )

    cycles = make_cycle_data(drawer, results)

    data = {
        'configs': trial_configs,
        'date': datetime.utcnow().strftime("%m-%d-%Y %H:%M"),
        'scale': svg_settings['scale'],
        'offset': svg_settings['offset'],
        'markerIds': tracksim.LimbProperty.LIMB_KEYS + [],
        'cycles': cycles.toDict(),
        'gals': make_formatted_gal_data(results),
        'separations': make_formatted_separation_data(results),
        'extensions': make_formatted_extension_data(results),
        'frames': make_animation_frame_data(drawer, results),
        'time': make_time_data(results),
        'limb_phases': track_definition.limb_phases.toDict(),
    }

    # Forces float rounding to behave so we don't end up with 1.20000000001
    # instead of 1.2
    storage = encoder.FLOAT_REPR
    encoder.FLOAT_REPR = lambda o: format(o, '%.12g')
    data = json.dumps(data)

    path = os.path.join(output_directory, '{}.json'.format(sim_id))
    with open(path, 'w+') as f:
        f.write(data)

    encoder.FLOAT_REPR = storage

    drawer.write(os.path.join(output_directory, '{}.svg'.format(sim_id)))

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
        for key in tracksim.LimbProperty.LIMB_KEYS:
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

    gait_cycles = tracksim.LimbProperty().assign([], [], [], [])
    positions = results['positions']
    steps = len(results['times'])

    for i in range(steps):
        for key in tracksim.LimbProperty.LIMB_KEYS:
            cycles = gait_cycles.get(key)
            pos = positions.get(key)[i]
            if not cycles or cycles[-1][1] != pos.annotation:
                cycles.append([1, pos.annotation])
            else:
                cycles[-1][0] += 1

    return gait_cycles

def make_formatted_gal_data(results):
    """

    :param results:
    :return:
    """

    values = []
    uncertainties = []
    data = results['gals']

    for v in data:
        values.append(v.value)
        uncertainties.append(v.uncertainty)

    mean = number.weighted_mean_and_deviation(*data)
    deviations = number.deviations(mean.value, data)

    return {
        'values':values,
        'deviation_max': number.round_to_order(max(deviations), -2),
        'uncertainties': uncertainties,
        'result': mean.html_label
    }

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

        mean = number.weighted_mean_and_deviation(*data)
        deviations = number.deviations(mean.value, data)

        out[key] = dict(
            values=values,
            deviation_max=number.round_to_order(max(deviations), -2),
            uncertainties=uncertainties,
            result=mean.html_label )

    return out

def make_formatted_extension_data(results):
    """

    :param results:
    :return:
    """

    out = {}
    for key in tracksim.LimbProperty.LIMB_KEYS:
        data = results['extensions'].get(key)
        values = []
        uncertainties = []

        for v in data:
            values.append(v.value)
            uncertainties.append(v.uncertainty)

        mean = number.weighted_mean_and_deviation(*data)
        deviations = number.deviations(mean.value, data)

        out[key] = dict(
            values=values,
            deviation_max=number.round_to_order(max(deviations), -2),
            uncertainties=uncertainties,
            result=mean.html_label )

    return out

def make_time_data(results):
    """

    :param results:
    :return:
    """

    count = len(results['times'])
    times = list(results['times'])
    progress = list(number.linear_space(0, 100.0, count))

    return {
        'count': count,
        'cycles': times,
        'progress': progress
    }

