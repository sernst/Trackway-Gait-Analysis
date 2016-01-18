
import os
import shutil
import json
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
    output_directory = tracksim.make_results_path('report', sim_id)

    if os.path.exists(output_directory):
        try:
            shutil.rmtree(output_directory)
            os.rmdir(output_directory)
        except Exception:
            pass
    os.makedirs(output_directory)

    drawer = svg.SvgWriter()
    draw.trackway_positions(track_definition.limb_positions, drawer)

    cycles = make_cycle_data(drawer, results)

    data = {
        'scale': drawer.scale,
        'offset': drawer.offset,
        'markerIds': tracksim.LimbProperty.LIMB_KEYS + [],
        'cycles': cycles.toDict(),
        'gals': make_formatted_gal_data(results),
        'extensions': make_formatted_extension_data(results),
        'frames': make_animation_frame_data(drawer, results),
        'time': make_time_data(results) }

    create_file_from_template(
        src_path=tracksim.make_resource_path('report', 'trial.js'),
        dest_path=os.path.join(output_directory, 'trial.js'),
        replacements={})

    create_file_from_template(
        src_path=tracksim.make_resource_path('report', 'plotly.js'),
        dest_path=os.path.join(output_directory, 'plotly.js'),
        replacements={})

    create_file_from_template(
        src_path=tracksim.make_resource_path('report', 'jquery.js'),
        dest_path=os.path.join(output_directory, 'jquery.js'),
        replacements={})

    create_file_from_template(
        src_path=tracksim.make_resource_path('report', 'trial.css'),
        dest_path=os.path.join(output_directory, 'trial.css'),
        replacements={})

    limb_phase_label = 'Pes: ({}, {}) Manus: ({}, {})'.format(
        *track_definition.limb_phases.values() )

    create_file_from_template(
        src_path=tracksim.make_resource_path('report', 'trial.html'),
        dest_path=os.path.join(output_directory, 'trial.html'),
        replacements={
            '###TITLE###': trial_configs['name'],
            '###SUMMARY###': trial_configs.get('summary', ''),
            '###DATE###': datetime.utcnow().strftime("%m-%d-%Y %H:%M"),
            '###DUTY_CYCLE###': str(round(100.0*trial_configs['duty_cycle'])),
            '###PHASES###': limb_phase_label,
            '###SVG###': drawer.dumps(),
            '\'###DATA###\'': json.dumps(data)
        })

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

    for key in tracksim.LimbProperty.LIMB_KEYS:
        style_name = '{}-marker'.format(key)
        style = {
            'fill': 'transparent',
            'stroke-width': '4px',
            'stroke': svg.SvgWriter.LIMB_COLORS.get(key) }
        if key.find('manus') != -1:
            style['stroke-dasharray'] = '4,4'

        drawer.add_style_definition('.{}'.format(style_name), style)
        drawer.draw_circle(0, 0, 12, style_name, name=key)

    positions = results['positions']
    steps = len(results['times'])
    frames = []

    for i in range(steps):
        frames.append({'time':results['times'][i], 'positions':[]})
        for key in tracksim.LimbProperty.LIMB_KEYS:
            pos = positions.get(key)[i]
            frames[-1]['positions'].append({
                'x':pos.x.value,
                'y':pos.y.value,
                'xunc': pos.x.uncertainty,
                'yunc': pos.y.uncertainty,
                'annotation': pos.annotation
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
            if not cycles or cycles[-1]['key'] != pos.annotation:
                cycles.append({
                    'key': pos.annotation,
                    'steps': 1
                })
            else:
                cycles[-1]['steps'] += 1

    return gait_cycles

def make_formatted_gal_data(results):
    """

    :param results:
    :return:
    """

    values = []
    uncertainties = []

    for v in results['gals']:
        values.append(v.value)
        uncertainties.append(v.uncertainty)

    return {
        'values':values,
        'uncertainties': uncertainties,
        'result': number.weighted_mean_and_deviation(
                *results['gals']).html_label
    }

def make_formatted_extension_data(results):
    """

    :param results:
    :return:
    """

    out = {}
    for key in ['left', 'right', 'front', 'back']:
        data = results['extensions'][key]
        values = []
        uncertainties = []

        for v in data:
            values.append(v.value)
            uncertainties.append(v.uncertainty)

        out[key] = dict(
            values=values,
            uncertainties=uncertainties,
            result=number.weighted_mean_and_deviation(*data).html_label )

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
        'progress': progress }

