import tracksim
from tracksim import reporting

def initialize(report_path:str = None, echo_groups:bool = False):

    try:
        from bokeh.plotting import output_notebook
        output_notebook()
    except Exception:
        print('bokeh plotting package required. Run the command:')
        print('$ conda install bokeh')
        raise

    print('PROJECT HOME:', tracksim.make_project_path())

    if report_path is None:
        report_path = tracksim.make_results_path('report')
    print('REPORT PATH:', report_path)

    if echo_groups:
        print('\nEXISTING GROUP REPORTS:')
        for item in reporting.list_results(report_path, trials=False):
            print('  * {}: {}'.format(item['id'], item['url']))

    return report_path
