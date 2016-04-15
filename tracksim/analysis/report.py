import os
import json
import random
from datetime import datetime

from jinja2 import Template

import tracksim
from tracksim.analysis import cacher

REPORT = []


def add_json(window_key, data):
    template = Template("""
        <script>
            window.{{ KEY }} = {{ DATA }};
        </script>
    """)

    REPORT.append(template.render(
        KEY=window_key,
        DATA=json.dumps(data)
    ))


def add_html(content):
    REPORT.append(content)


def add_table(data_frame):

    table_id = 'table-{}-{}'.format(
        datetime.utcnow().strftime('%H-%M-%S-%f'),
        random.randint(0, 1e8)
    )

    template = Template("""
        <div id="{{id}}" class="table"></div>
        <script>
        (function () {
            var data = [
                ["", "Kia", "Nissan", "Toyota", "Honda"],
                ["2008", 10, 11, 12, 13],
                ["2009", 20, 11, 14, 13],
                ["2010", 30, 15, 12, 13]
            ];

            var container = document.getElementById('{{id}}');
            new Handsontable(container, {
                data: data,
                stretchH: 'all'
            });
        }());
        </script>
        """)

    REPORT.append(template.render(
        id=table_id
    ))


def write_report(path) -> str:
    """

    :param path:
    :return:
    """

    if len(REPORT) < 1:
        return None

    path = os.path.join(path, '{analysis_id}.html'.format(
        analysis_id=cacher.fetch('__analysis_id__')
    ))

    with open(tracksim.make_results_path('analysis.html'), 'r+') as f:
        template = Template(f.read())

    with open(path, 'w+') as f:
        f.write(template.render(BODY='\n'.join(REPORT)))

    while len(REPORT) > 0:
        REPORT.pop()

    return path
