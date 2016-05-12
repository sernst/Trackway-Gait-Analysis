import os
import typing
from datetime import datetime

import measurement_stats as mstats

from tracksim import configs
from tracksim import limb
from tracksim import paths
from tracksim import reporting
from tracksim import svg
from tracksim import trackway
from tracksim.svg import draw
from tracksim.trial.analyze import advancement
from tracksim.trial.analyze import coupling
from tracksim.trial.analyze import separation


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
    times = make_time_data(time_steps, settings)
    coupling_data = coupling.calculate(foot_positions, times)
    separation_data = separation.calculate(foot_positions, times)
    advancement_data = advancement.calculate(foot_positions, times)

    report = reporting.Report('trial', sim_id)
    add_header_section(report, settings, track_definition.activity_phases)
    svg_settings = add_svg(sim_id, report, track_definition, foot_positions)
    add_info(report, settings, coupling_data)
    coupling.add_to_report(report, coupling_data, times)
    advancement.add_to_report(report, advancement_data, times)
    separation.add_to_report(report, separation_data, times)
    report.add_whitespace(10)

    report.add_data(
        # Used in the header display
        time=times,
        cycles=make_cycle_data(foot_positions, times).to_dict(),

        # Used in animating the SVG
        scale=svg_settings['scale'],
        offset=svg_settings['offset'],
        markerIds=limb.KEYS + [],
        frames=make_animation_frame_data(foot_positions, coupling_data, times)
    )

    url = report.write()
    write_data(
        path=os.path.join(report.directory, '{}.json'.format(sim_id)),
        settings=settings,
        trackway_definition=track_definition,
        foot_positions=foot_positions,
        times=times,
        coupling_data=coupling_data,
        advancement_data=advancement_data
    )

    return url


def write_data(
        path: str,
        settings: dict,
        trackway_definition: trackway.TrackwayDefinition,
        foot_positions: limb.Property,
        times: dict,
        coupling_data: dict,
        advancement_data: dict
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
    :param advancement_data:
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
        couplings=coupling.serialize(coupling_data),
        advancement=advancement.serialize(advancement_data)
    ))


def add_header_section(
        report: reporting.Report,
        settings: dict,
        activity_phases: limb.Property
):
    """

    :param report:
    :param settings:
    :param activity_phases:
    :return:
    """

    activity_phases = activity_phases.values()
    support_phases = settings['support_phases']

    activity_phases = ['{}%'.format(round(100 * x)) for x in activity_phases]
    support_phases = ['{}%'.format(round(100 * x)) for x in support_phases]

    report.add_template(
        paths.resource('trial', 'header.html'),
        title=settings.get('name'),
        summary=settings.get('summary'),
        duty_cycle=round(100.0 * settings['duty_cycle']),
        activity_phases=activity_phases,
        support_phases=support_phases,
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

    dom_template = """
        <div class="svg-box">
          {{ svg }}
          <div class="svg-controls-box" style="display:none">
            <div>
                <div>Activity: <span class="activity-status"></span></div>
                <div>Support: <span class="support-status"></span></div>
            </div>
            <div class="spacer"></div>
          </div>
        </div>
        """

    report.add_svg(
        drawer.dumps(),
        filename='{}.svg'.format(sim_id),
        dom_template=dom_template
    )

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
        paths.resource('trial', 'info.html'),
        coupling_length=coupling_data['value'].html_label,
        coupling_bounds=bounds
    )


def make_animation_frame_data(
        foot_positions: limb.Property,
        coupling_data: dict,
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

    :param coupling_data:
    :param foot_positions:
        The simulation results
    :param times:
        Time step information
    """

    frames = []

    for i in range(times['count']):
        positions = []
        for key in limb.KEYS:
            pos = foot_positions.get(key)[i]
            positions.append({
                'x': [pos.x.value, pos.x.uncertainty, pos.x.raw],
                'y': [pos.y.value, pos.y.uncertainty, pos.y.raw],
                'f': pos.annotation
            })

        rear = coupling_data['rear'][i]
        forward = coupling_data['forward'][i]
        midpoint = coupling_data['midpoints'][i]

        frames.append(dict(
            time=times['cycles'][i],
            support_time=times['support_cycles'][i],
            positions=positions,
            rear_coupler={
                'x': [rear.x.value, rear.x.uncertainty, rear.x.raw],
                'y': [rear.y.value, rear.y.uncertainty, rear.y.raw]
            },
            forward_coupler={
                'x': [forward.x.value, forward.x.uncertainty, forward.x.raw],
                'y': [forward.y.value, forward.y.uncertainty, forward.y.raw]
            },
            midpoint={
                'x': [midpoint.x.value, midpoint.x.uncertainty, midpoint.x.raw],
                'y': [midpoint.y.value, midpoint.y.uncertainty, midpoint.y.raw]
            }
        ))

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


def make_time_data(times: list, settings: dict) -> dict:
    """
    Creates a dictionary with temporal information about the simulation for
    use in the report. The returned dictionary contains:

        - count: The number of time steps in the simulation
        - times: A list of floating point time steps in the simulation
        - progress: A list of percent progress for each time step in the
            simulation

    :param times:
        Simulation time step list
    :param settings:
    """

    dc = settings['duty_cycle']
    support_cycles = [configs.time_to_support_time(t, dc) for t in times]

    return dict(
        count=len(times),
        cycles=times,
        support_cycles=support_cycles,
        steps_per_cycle=settings['steps_per_cycle'],
        progress=list(mstats.ops.linear_space(0, 100.0, len(times)))
    )

