import tracksim
from tracksim import reporting


def initialize(report_path:str = None, echo_groups:bool = False) -> str:
    """
    Runs interactive notebook initialization and returns the report path for
    the interactive session

    :param report_path:
        The report path to use in the application. If none is specified, the
        default value will be used
    :param echo_groups:
        Whether or not you want to echo the existing group reports in the
        specified report path
    """

    print('PROJECT HOME:', tracksim.make_project_path())

    if report_path is None:
        report_path = tracksim.load_configs().get('path.notebook.report')

    if report_path is None:
        report_path = tracksim.make_reports_path()

    print('REPORT PATH:', report_path)

    if echo_groups:
        print('\nEXISTING GROUP REPORTS:')
        for item in reporting.list_results(report_path, trials=False):
            print('  * {}: {}'.format(item['id'], item['url']))

    return report_path
