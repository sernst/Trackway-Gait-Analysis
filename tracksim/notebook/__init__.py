import tracksim
from tracksim import reporting


def initialize(results_path:str = None, echo_groups:bool = False) -> str:
    """
    Runs interactive notebook initialization and returns the report path for
    the interactive session

    :param results_path:
        The results path to use in the application. If none is specified, the
        default value will be used
    :param echo_groups:
        Whether or not you want to echo the existing group reports in the
        specified report path
    """

    print('PROJECT ROOT:', tracksim.make_project_path())

    if results_path is None:
        results_path = tracksim.load_configs().get('path.notebook.report')

    if results_path is None:
        results_path = tracksim.make_results_path()

    print('RESULTS ROOT:', results_path)

    if echo_groups:
        print('\nEXISTING GROUP REPORTS:')
        for item in reporting.list_results(results_path, trials=False):
            print('  * {}: {}'.format(item['id'], item['url']))

    return results_path
