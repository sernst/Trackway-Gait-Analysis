import json
import os
import random
import shutil
from datetime import datetime

import markdown
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template

from tracksim import paths

try:
    import plotly
except ImportError:
    plotly = None


class Report(object):
    """
    A class for storing the elements of the
    """

    def __init__(self, report_type:str, identifier: str = None, **kwargs):
        self.env = Environment(
            loader=FileSystemLoader(paths.resource('reports'))
        )

        self.id = identifier
        self.type = report_type
        self.body = []
        self.data = kwargs.get('data', {})
        self.files = dict()

    @property
    def url(self):
        """
        Returns the URL that will open this report file in the browser for
        viewing
        :return:
        """
        return 'file://{path}?id={id}'.format(
            path=paths.results('{}.html'.format(self.type)),
            id=self.id
        )

    @property
    def directory(self):
        """
        Returns the directory where the report file will be written
        :return:
        """
        return paths.results('reports', self.type, self.id)

    def add_header(self, level, text):
        """

        :param level:
        :param text:
        :return:
        """

        template = Template('<h{{level}}>{{text}}</h{{level}}>')

        self.body.append(template.render(level=level, text=text))

    def add_plaintext(self, text):
        """

        :param text:
        :return:
        """

        lines = text.strip().split('\n')

        for index in range(len(lines)):
            l = lines[index].strip()
            if len(l) < 1:
                l = '</p><p class="plaintextbox">'
            lines[index] = l

        self.body.append(
            '<p class="plaintextbox">{text}</p>'.format(text=' '.join(lines))
        )

    def add_markdown(self, source):
        """

        :param source:
        :return:
        """

        template = Template('<div class="textbox">{{ text }}</div>')

        self.body.append(template.render(
            text=markdown.markdown(source)
        ))

    def add_json(self, window_key, data):
        """

        :param window_key:
        :param data:
        :return:
        """

        template = Template("""
            <script>
                window.{{ KEY }} = {{ DATA }};
            </script>
        """)

        self.body.append(template.render(
            KEY=window_key,
            DATA=json.dumps(data)
        ))

    def add_html(self, content):
        """

        :param content:
        :return:
        """

        template = Template('<div class="box">{{content}}</div>')

        self.body.append(template.render(content=content))

    def add_plotly(self, data, layout):
        """

        :param data:
        :param layout:
        :return:
        """

        if plotly is None:
            raise ImportError('Unable to import Plotly library')

        self.add_html(plotly.offline.plot(
            {'data': data, 'layout': layout},
            output_type='div',
            include_plotlyjs=False
        ))

    def add_table(self, data_frame):
        """

        :param data_frame:
        :return:
        """

        table_id = 'table-{}-{}'.format(
            datetime.utcnow().strftime('%H-%M-%S-%f'),
            random.randint(0, 1e8)
        )

        column_headers = data_frame.columns.tolist()
        column_headers = ['"{}"'.format(x) for x in column_headers]

        data = []

        for index, row in data_frame.iterrows():
            data.append(row.tolist())

        template = self.env.get_template('body_table.template')
        self.body.append(template.render(
            id=table_id,
            data=json.dumps(data),
            column_headers=', '.join(column_headers)
        ))

    def write(self, results_path: str = None) -> str:
        """

        :param results_path:
        :return:
        """

        if len(self.body) < 1:
            return None

        if not results_path:
            results_path = paths.results()

        path = os.path.join(results_path, 'reports', self.type, self.id)

        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except Exception:
                try:
                    shutil.rmtree(path)
                except Exception:
                    return None

        os.makedirs(path)

        template = self.env.get_template('report.template')

        report_path = os.path.join(path, '{}.js'.format(self.id))
        with open(report_path, 'w+') as f:
            f.write(template.render(
                DATA=json.dumps({
                    'data': self.data,
                    'body': '\n'.join(self.body)
                })
            ))

        for filename, contents in self.files.items():
            file_path = os.path.join(path, filename)
            with open(file_path, 'w+') as f:
                f.write(contents)

        return self.url

    def add_svg(self, svg:str, filename: str = None, dom_template = None):
        """

        :param svg:
        :param filename:
        :param dom_template:
        :return:
        """

        if dom_template is None:
            dom_template = """
                <div class="svg-box">
                    <div class="svg-box-inner">
                    {{ svg }}
                    </div>
                </div>
                """

        template = Template(dom_template)
        self.body.append(template.render(svg=svg))

        if not filename:
            return

        if not filename.endswith('.svg'):
            filename += '.svg'

        self.files[filename] = svg

    def add_template(self, path, **kwargs):
        """

        :param path:
        :param kwargs:
        :return:
        """

        with open(path, 'r+') as f:
            contents = f.read()

        self.body.append(Template(contents).render(**kwargs))

    def add_data(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

        for key, value in kwargs.items():
            self.data[key] = value

    def add_whitespace(self, lines: float = 1.0):
        """

        :param lines:
        :return:
        """

        pixels = round(12 * lines)
        self.body.append('<div style="height:{}px"> </div>'.format(pixels))
