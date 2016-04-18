import typing
from datetime import datetime

import plotly.graph_objs as go

import measurement_stats as mstats

import tracksim
from tracksim import limb
from tracksim import reporting
from tracksim import svg
from tracksim import trackway
from tracksim.reporting import plotting
from tracksim.svg import draw


def create(
        settings: dict,
        track_definition: trackway.TrackwayDefinition,
        sim_results: dict
) -> dict:
    """
    Creates a report based on the simulated trial data and saves that data
    to the report directory as well as returning the data:

    :param settings:
        Configuration for the trial being reported
    :param track_definition:
        The trackway source that was used by the simulation
    :param sim_results:
        Results dictionary created during simulation
    """

    sim_id = settings['name'].replace(' ', '-')
    time_data = make_time_data(sim_results)

    report = reporting.Report('trial', sim_id)
    add_header_section(report, settings, track_definition)

    drawer = svg.SvgWriter(padding=5)
    svg_settings = draw.trackway_positions(
        limb_positions=track_definition.limb_positions,
        positions=sim_results['positions'],
        drawer=drawer
    )
    report.add_svg(drawer.dumps(), filename='{}.svg'.format(sim_id))

    add_info(report, settings, sim_results)
    add_coupling_plots(report, sim_results, time_data)

    data = {
        # Used in the header display
        'time': time_data,
        'cycles': make_cycle_data(sim_results).to_dict(),

        # Used in animating the SVG
        'scale': svg_settings['scale'],
        'offset': svg_settings['offset'],
        'markerIds': limb.KEYS + [],
        'frames': make_animation_frame_data(sim_results)
    }

    report.add_data(**data)
    report.add_whitespace(10)
    report.write()

    return {
        'url': report.url,
        'data': data
    }


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


def add_info(report: reporting.Report, settings: dict, results: dict):
    """
    Adds the info section to the report, which is an existing html template
    that is pre-populated with data by rendering it with Jinja2

    :param report:
        The report being created
    :param settings:
        Configuration settings for the trial simulation
    :param results:
        Results from the trial simulation
    :return:
    """

    coupling_data = results['couplings']

    bounds = coupling_data['bounds']
    bounds = [mstats.value.round_significant(b, 4) for b in bounds]

    report.add_template(
        tracksim.make_resource_path('trial', 'info.html'),
        coupling_length=coupling_data['value'].html_label,
        coupling_length_deviation=coupling_data['deviation_max'],
        coupling_bounds=bounds
    )

def add_coupling_plots(
        report: reporting.Report,
        results: dict,
        time_data: dict
):
    """

    :param report:
    :param results:
    :param time_data:
    :return:
    """

    data = results['couplings']
    values, uncertainties = mstats.values.unzip(data['data'])

    plot = plotting.make_line_data(
        time_data['progress'],
        values,
        uncertainties
    )

    report.add_plotly(
        data=plot['data'],
        layout=plotting.create_layout(
            plot['layout'],
            'Coupling Length',
            'Progress (%)',
            'Length (m)'
        )
    )

    report.add_plotly(
        data=[go.Scatter(
            x=data['distribution_profile']['x'],
            y=data['distribution_profile']['y'],
            mode='lines'
        )],
        layout=plotting.create_layout(
            title='Coupling Length Distribution',
            x_label='Coupling Distance (m)',
            y_label='Normalized Probability Density (au)'
        )
    )


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

