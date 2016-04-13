import os
import typing
from datetime import datetime

import measurement_stats as mstats

from tracksim import limb
from tracksim import reporting
from tracksim import svg
from tracksim import trackway
from tracksim.svg import draw


def create(
        settings: dict,
        track_definition: trackway.TrackwayDefinition,
        sim_results: dict
) -> dict:
    """
    Creates a report based on the simulated trial data and saves that data
    to the report directory as well as returning the data:

        * cycles: dict
          * right_pes: list[N-Cycles]
            * list number[2]
          * left_pes: list[N-Cycles]
            * list number[2]
          * left_manus: list[N-Cycles]
            * list number[2]
          * right_manus: list[N-Cycles]
            * list number[2]
        * scale: number
        * separations: dict
          * back: dict
            * values: list number[N]
            * result: str
            * uncertainties: list number[N]
            * value: list number[2]
          * left: dict
            * values: list number[N]
            * result: str
            * uncertainties: list number[N]
            * value: list number[2]
          * right: dict
            * values: list number[N]
            * result: str
            * uncertainties: list number[N]
            * value: list number[2]
          * front: dict
            * values: list number[N]
            * result: str
            * uncertainties: list number[N]
            * value: list number[2]
        * limb_phases: dict
          * right_pes: number
          * left_pes: number
          * left_manus: number
          * right_manus: number
        * svg: str
        * time: dict
          * cycles: list number[N]
          * count: number
          * progress: list number[N]
        * markerIds: list str[4]
        * root_path: str
        * url: str
        * offset: list number[2]
        * id: str
        * date: str
        * couplings: dict
          * values: list number[N]
          * result: str
          * uncertainties: list number[N]
          * bounds: dict
            * two_sigma: list number[2]
            * one_sigma: list number[2]
          * deviation_max: number
        * extensions: dict
          * right_pes: dict
            * values: list number[N]
            * result: str
            * uncertainties: list number[N]
            * value: list number[2]
          * left_pes: dict
            * values: list number[N]
            * result: str
            * uncertainties: list number[N]
            * value: list number[2]
          * left_manus: dict
            * values: list number[N]
            * result: str
            * uncertainties: list number[N]
            * value: list number[2]
          * right_manus: dict
            * values: list number[N]
            * result: str
            * uncertainties: list number[N]
            * value: list number[2]
        * frames: list dict[N]
          * time: number
          * positions: list dict[4]
            * f: str
            * x: list number[2]
            * y: list number[2]
        * configs: dict

    :param settings:
        Configuration for the trial being reported
    :param track_definition:
        The trackway source that was used by the simulation
    :param sim_results:
        Results dictionary created during simulation
    """

    root_report_path = reporting.initialize_output_directory(
        settings.get('report_path')
    )

    sim_id = settings['name'].replace(' ', '-')
    output_directory = os.path.join(root_report_path, 'trials', sim_id)

    drawer = svg.SvgWriter(padding=5)
    svg_settings = draw.trackway_positions(
        limb_positions=track_definition.limb_positions,
        positions=sim_results['positions'],
        drawer=drawer
    )

    url = 'file://{root_path}/trial.html?id={id}'.format(
        root_path=root_report_path,
        id=sim_id
    )

    data = {
        'root_path': root_report_path,
        'id': sim_id,
        'url': url,
        'configs': settings,
        'date': datetime.utcnow().strftime("%m-%d-%Y %H:%M"),
        'scale': svg_settings['scale'],
        'offset': svg_settings['offset'],
        'markerIds': limb.KEYS + [],
        'cycles': make_cycle_data(sim_results).to_dict(),
        'couplings': make_formatted_coupling_data(sim_results),
        'separations': make_formatted_separation_data(sim_results),
        'extensions': make_formatted_extension_data(sim_results).to_dict(),
        'frames': make_animation_frame_data(sim_results),
        'time': make_time_data(sim_results),
        'limb_phases': track_definition.limb_phases.to_dict(),
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


def create_file_from_template(
        template_path: str,
        dest_path: str,
        replacements: dict
) -> str:
    """
    Loads a source template file at the specified src_path and saves it to the
    destination path with substitutions made for the replacement keys and
    values

    :param template_path:
        Path to the template source file
    :param dest_path:
        Path where the modified file should be saved
    :param replacements:
        A dictionary containing the replacements that should be made in the
        modified file. The method searches the source file for each occurrence
        of each key in the replacements dictionary and replaces it with the
        value for that key
    """

    with open(template_path, 'r+') as f:
        contents = f.read()

    for key, value in replacements.items():
        contents = contents.replace(key, value)

    with open(dest_path, 'w+') as f:
        f.write(contents)

    return dest_path


def make_animation_frame_data(sim_results: dict) -> typing.List[dict]:
    """
    Creates a list of animation frame data from the results, which is used by
    the JavaScript report to animate the feet within the trackway. Each frame
    in the returned list contains:

    - time: The simulation time for the frame
    - positions: An ordered list of position dictionaries for each limb, where
        the order is defined by the limb.KEYS order. Each dictionary contains:
            - x: A list where x[0] is the position and x[1] is the uncertainty
            - y: A list where y[0] is the position and y[1] is the uncertainty
            - f: The enumerated annotation for the position

    :param sim_results:
        The simulation results dictionary
    """

    positions = sim_results['positions']
    steps = len(sim_results['times'])
    frames = []

    for i in range(steps):
        frames.append({'time':sim_results['times'][i], 'positions':[]})
        for key in limb.KEYS:
            pos = positions.get(key)[i]
            frames[-1]['positions'].append({
                'x':[pos.x.value, pos.x.uncertainty],
                'y':[pos.y.value, pos.y.uncertainty],
                'f': pos.annotation
            })

    return frames


def make_cycle_data(sim_results: dict) -> limb.Property:
    """
    Trial report pages contain a duty-cycle diagram, which is created using the
    data generated in this method. The returned limb.Property contains a list
    for each limb of the duty cycle regions for that limb where a region is a
    list with elements:
        - 0: The time at which this cycle ends
        - 1: The enumerated annotation for this cycle

    :param sim_results:
        Simulation results dictionary
    """

    gait_cycles = limb.Property().assign([], [], [], [])
    positions = sim_results['positions']
    steps = len(sim_results['times'])

    for i in range(steps):
        for key in limb.KEYS:
            cycles = gait_cycles.get(key)
            pos = positions.get(key)[i]
            if not cycles or cycles[-1][1] != pos.annotation:
                cycles.append([1, pos.annotation])
            else:
                cycles[-1][0] += 1

    return gait_cycles


def make_formatted_coupling_data(sim_results: dict) -> dict:
    """
    Creates a dictionary that contains coupling length data formatted for
    display within the report. The returned dictionary contains:

        - values: A list of coupling length values (floats) at each time
            within the simulation
        - uncertainties: A list of coupling length uncertainties (floats) for
            each time within the simulation
        - deviation_max: The largest sigma deviation value between two values
            in the coupling values array
        - result: The median coupling length value formatted for html display
        - bounds: The bounds data object that contains information about the
            valid regions for the coupling lengths

    :param sim_results:
        Simulation results dictionary
    """

    data = sim_results['couplings']
    values, uncertainties = mstats.values.unzip(data['data'])

    return dict(
        values=values,
        uncertainties=uncertainties,
        deviation_max=data['deviation_max'],
        result=data['value'].html_label,
        bounds=data['bounds']
    )


def make_formatted_separation_data(sim_results: dict) -> dict:
    """
    Generates a dictionary of formatted results for the report about the
    separation data between limb pair combinations left side, right side,
    back and front. The resulting dictionary has four keys 'left', 'right',
    'back' and 'front' with combination data for each limb pair. Each
    combination value is a dictionary containing:

        - values: The separation values for that limb pair at each time within
            the simulation
        - uncertainties: The separation uncertainty values for each time within
            the simulation
        - result: Html formatted label for the weighted average value of the
            separations
        - value: A list containing [mean value, mean uncertainty]

    :param sim_results:
        Simulation results dictionary
    """

    out = {}
    for key in ['left', 'right', 'front', 'back']:
        data = sim_results['separations'][key]
        values = []
        uncertainties = []

        for v in data:
            values.append(v.value)
            uncertainties.append(v.uncertainty)

        mean = mstats.mean.weighted_mean_and_deviation(*data)

        out[key] = dict(
            values=values,
            uncertainties=uncertainties,
            result=mean.html_label,
            value=[mean.value, mean.uncertainty]
        )

    return out


def make_formatted_extension_data(sim_results: dict) -> limb.Property:
    """
    Generates a dictionary of formatted results for the report about the
    extension data for each limb. The returned limb property contains
    a dictionary for each limb that contains:

        - values: The extension values for that limb at each time in the
            simulation
        - uncertainties: The extension uncertainty values for each time within
            the simulation
        - result: Html formatted label for the weighted average value of the
            extension
        - value: A list containing [mean value, mean uncertainty]

    :param sim_results:
        Simulation results dictionary
    """

    out = limb.Property()
    for key in limb.KEYS:
        data = sim_results['extensions'].get(key)
        values = []
        uncertainties = []

        for v in data:
            values.append(v.value)
            uncertainties.append(v.uncertainty)

        mean = mstats.mean.weighted_mean_and_deviation(*data)

        out.set(key, dict(
            values=values,
            uncertainties=uncertainties,
            result=mean.html_label,
            value=[mean.value, mean.uncertainty]
        ))

    return out


def make_time_data(sim_results: dict) -> dict:
    """
    Creates a dictionary with temporal information about the simulation for
    use in the report. The returned dictionary contains:

        - count: The number of time steps in the simulation
        - times: A list of floating point time steps in the simulation
        - progress: A list of percent progress for each time step in the
            simulation

    :param sim_results:
        Simulation results dictionary
    """

    count = len(sim_results['times'])
    times = list(sim_results['times'])
    progress = list(mstats.ops.linear_space(0, 100.0, count))

    return {
        'count': count,
        'cycles': times,
        'progress': progress
    }

