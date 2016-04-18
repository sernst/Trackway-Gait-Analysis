import os
import typing
from datetime import datetime

import measurement_stats as mstats

import tracksim
from tracksim import limb
from tracksim import reporting
from tracksim import svg
from tracksim import trackway
from tracksim.svg import draw
from tracksim.trial.analyze import coupling


def create(
        settings: dict,
        track_definition: trackway.TrackwayDefinition,
        foot_positions: limb.Property,
        time_steps: typing.List[float]
) -> dict:
    """
    Analyzed the simulated trial data and saves and saves that data as well as
    a report for consumption

    :param settings:
        Configuration for the trial being reported
    :param track_definition:
        The trackway source that was used by the simulation
    :param foot_positions:
        The positions of each foot calculated during the simulation
    :param time_steps:
        A list of time steps (in cycles) for the simulation
    """

    sim_id = settings['id']
    times = make_time_data(time_steps)
    coupling_data = coupling.calculate(foot_positions)

    report = reporting.Report('trial', sim_id)
    add_header_section(report, settings, track_definition)
    svg_settings = add_svg(sim_id, report, track_definition, foot_positions)
    add_info(report, settings, coupling_data)
    coupling.add_to_report(report, coupling_data, times)
    report.add_whitespace(10)

    report.add_data(
        # Used in the header display
        time=times,
        cycles=make_cycle_data(foot_positions, times).to_dict(),

        # Used in animating the SVG
        scale=svg_settings['scale'],
        offset=svg_settings['offset'],
        markerIds=limb.KEYS + [],
        frames=make_animation_frame_data(foot_positions, times)
    )

    url = report.write()
    write_data(
        path=os.path.join(report.directory, '{}.json'.format(sim_id)),
        settings=settings,
        trackway_definition=track_definition,
        foot_positions=foot_positions,
        times=times,
        coupling_data=coupling_data
    )

    return url


def write_data(
        path: str,
        settings: dict,
        trackway_definition: trackway.TrackwayDefinition,
        foot_positions: limb.Property,
        times: dict,
        coupling_data: dict
):
    """
    Writes a JSON serialized data file containing the results of the trial for
    later analysis

    :param path:
    :param settings:
    :param trackway_definition:
    :param foot_positions:
    :param times:
    :param coupling_data:
    :return:
    """

    position_data = dict()
    for limb_id, positions in foot_positions.items():
        position_data[limb_id] = [x.to_dict() for x in positions]

    track_data = dict()
    for limb_id, positions in trackway_definition.limb_positions.items():
        track_data[limb_id] = [x.to_dict() for x in positions]

    reporting.write_json_results(path, dict(
        settings=settings,
        times=times,
        foot_positions=position_data,
        track_positions=track_data,
        couplings=coupling.serialize(coupling_data)
    ))


def add_header_section(
        report: reporting.Report,
        settings: dict,
        track_definition: trackway.TrackwayDefinition
):
    """

    :param report:
    :param settings:
    :param track_definition:
    :return:
    """

    phases = track_definition.limb_phases.values()
    phases = ['{}%'.format(round(100 * x)) for x in phases]

    report.add_template(
        tracksim.make_resource_path('trial', 'header.html'),
        title=settings.get('name'),
        summary=settings.get('summary'),
        duty_cycle=settings.get('duty_cycle'),
        limb_phases=phases,
        date=datetime.utcnow().strftime("%m-%d-%Y %H:%M")
    )


def add_svg(
        sim_id: str,
        report: reporting.Report,
        track_definition: trackway.TrackwayDefinition,
        foot_positions: limb.Property
):
    """

    :param sim_id:
    :param report:
    :param track_definition:
    :param foot_positions:
    :return:
    """

    drawer = svg.SvgWriter(padding=5)
    svg_settings = draw.trackway_positions(
        limb_positions=track_definition.limb_positions,
        positions=foot_positions,
        drawer=drawer
    )
    report.add_svg(drawer.dumps(), filename='{}.svg'.format(sim_id))

    return svg_settings


def add_info(report: reporting.Report, settings: dict, coupling_data: dict):
    """
    Adds the info section to the report, which is an existing html template
    that is pre-populated with data by rendering it with Jinja2

    :param report:
        The report being created
    :param settings:
        Configuration settings for the trial simulation
    :param coupling_data:
        Coupling analysis data
    :return:
    """

    bounds = coupling_data['bounds']
    bounds = [mstats.value.round_significant(b, 4) for b in bounds]

    report.add_template(
        tracksim.make_resource_path('trial', 'info.html'),
        coupling_length=coupling_data['value'].html_label,
        coupling_bounds=bounds
    )


def make_animation_frame_data(
        foot_positions: limb.Property,
        times: dict
) -> typing.List[dict]:
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

    :param foot_positions:
        The simulation results
    :param times:
        Time step information
    """

    frames = []

    for i in range(times['count']):
        frames.append({'time': times['cycles'][i], 'positions': []})
        for key in limb.KEYS:
            pos = foot_positions.get(key)[i]
            frames[-1]['positions'].append({
                'x': [pos.x.value, pos.x.uncertainty],
                'y': [pos.y.value, pos.y.uncertainty],
                'f': pos.annotation
            })

    return frames


def make_cycle_data(
        foot_positions: limb.Property,
        times: dict
) -> limb.Property:
    """
    Trial report pages contain a duty-cycle diagram, which is created using the
    data generated in this method. The returned limb.Property contains a list
    for each limb of the duty cycle regions for that limb where a region is a
    list with elements:
        - 0: The time at which this cycle ends
        - 1: The enumerated annotation for this cycle

    :param foot_positions:
        Simulation results
    :param times:
        Time step information
    """

    gait_cycles = limb.Property().assign([], [], [], [])

    for i in range(times['count']):
        for key in limb.KEYS:
            cycles = gait_cycles.get(key)
            pos = foot_positions.get(key)[i]
            if not cycles or cycles[-1][1] != pos.annotation:
                cycles.append([1, pos.annotation])
            else:
                cycles[-1][0] += 1

    return gait_cycles


def make_time_data(times: list) -> dict:
    """
    Creates a dictionary with temporal information about the simulation for
    use in the report. The returned dictionary contains:

        - count: The number of time steps in the simulation
        - times: A list of floating point time steps in the simulation
        - progress: A list of percent progress for each time step in the
            simulation

    :param times:
        Simulation time step lise
    """

    return {
        'count': len(times),
        'cycles': times,
        'progress': list(mstats.ops.linear_space(0, 100.0, len(times)))
    }

