import os
import typing
import json
from datetime import datetime

import tracksim
from tracksim import reporting
from tracksim.reporting import plotting


def create(
        settings: dict,
        trials: typing.List[dict]
) -> dict:
    """
    Creates a group report dictionary and writes it to the group report
    directory as well as returning it.

    :param settings:
        Configuration for the group
    :param trials:
        List of trial simulation results
    """

    group_id = settings['id']
    report = reporting.Report('group', group_id)

    add_header_section(report, settings, trials)
    add_coupling_plots(report, trials)

    report.add_whitespace(10)
    report.write()

    reporting.write_json_results(
        path=os.path.join(report.directory, '{}.json'.format(group_id)),
        data=dict(
            trials=trials,
            settings=settings
        )
    )

    return report.url


def add_header_section(
        report: reporting.Report,
        settings: dict,
        trials: typing.List[dict]
):
    trial_data = []
    for t in trials:
        color = plotting.get_color(t['index'] - 1, as_string=True)

        trial_data.append(dict(
            index=t['index'],
            id=t['id'],
            name=t['settings']['name'],
            summary=t['settings'].get('summary', ''),
            back_color=color
        ))

    report.add_template(
        path=tracksim.make_resource_path('group', 'header.html'),
        title=settings['name'],
        date=datetime.utcnow().strftime("%m-%d-%Y %H:%M"),
        summary=settings.get('summary'),
        trials=trial_data
    )


def add_coupling_plots(
        report: reporting.Report,
        trials: typing.List[dict]
):
    """
    Generates coupling report data from the analyzed coupling data and the
    individual simulation trial results

    :param report:
        Grouped coupling data from the grouped simulation results
    :param trials:
        Simulation results for each trial run by the group
    """

    distribution_traces = []
    population_traces = []
    index = 0

    for trial in trials:

        path = tracksim.make_results_path(
            'reports', 'trial', trial['id'], '{}.json'.format(trial['id'])
        )
        with open(path, 'r+') as f:
            trial_data = json.load(f)

        index += 1
        coupling_data = trial_data['couplings']

        distribution_traces.append(dict(
            x=coupling_data['distribution_profile']['x'],
            y=coupling_data['distribution_profile']['y'],
            type='scatter',
            mode='lines',
            name='{}'.format(index)
        ))

        population_traces.append(dict(
            x=coupling_data['population'],
            type='box',
            name='{}'.format(index),
            boxpoints=False
        ))

    report.add_plotly(
        data=distribution_traces,
        layout=plotting.create_layout(
            title='Coupling Length Trial Distributions',
            x_label='Expectation Value (au)',
            y_label='Coupling Length (m)'
        )
    )

    report.add_plotly(
        data=population_traces,
        layout=plotting.create_layout(
            title='Coupling Length Trials',
            x_label='Coupling Length (m)',
            y_label='Trial Index (#)'
        )
    )

