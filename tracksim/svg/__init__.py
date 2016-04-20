import math
import random
from textwrap import dedent

import six

from tracksim import limb


class SvgWriter(object):

    PREFIX = """
    <svg version="1.1"
        id="###NAME###"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="###VIEW_BOX###">
    """

    SUFFIX = "</svg>"

    STYLE_PREFIX = '<style>\n/* <![CDATA[ */'
    STYLE_SUFFIX = '/* ]]> */\n</style>'

    LIMB_COLORS = limb.Property(
        left_pes='DodgerBlue',
        right_pes='DarkOrange',
        left_manus='DarkOliveGreen',
        right_manus='DarkOrchid' )

    def __init__(self, **kwargs):
        self.padding = kwargs.get('padding', 0)
        self.elements = []
        self.styles = []
        self.name = 'svg-{}'.format(random.randint(0, 1e12))

    def add_style_definition(self, classifier, styles):
        """

        :param classifier:
        :param styles:
        :return:
        """
        self.styles.append(dict(name=classifier, styles=styles))

    def draw_circle(self, x, y, radius, classes, name=None, data=None):
        """

        :param x:
        :param y:
        :param radius:
        :param classes:
        :param name:
        :return:
        """

        self.add_element(
            bounds=[x - radius, y - radius, x + radius, y + radius],
            name=name,
            tag_name='circle',
            x_attrs=dict(cx=x),
            y_attrs=dict(cy=y),
            attrs=dict(r=radius),
            classes=classes,
            data=data
        )

    def add_element(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        self.elements.append(kwargs)

    def calculate_global_bounds(self):
        """

        :return:
        """
        b = [1e12, 1e12, -1e12, -1e12]
        for element in self.elements:
            element_bounds = element.get('bounds')
            if element_bounds:
                b[0] = math.floor(min(element_bounds[0], b[0]))
                b[1] = math.floor(min(element_bounds[1], b[1]))
                b[2] = math.ceil(max(element_bounds[2], b[2]))
                b[3] = math.ceil(max(element_bounds[3], b[3]))

        b[0] -= self.padding
        b[1] -= self.padding
        b[2] += self.padding - b[0]
        b[3] += self.padding - b[1]

        return b

    def dumps(self):
        """

        :return:
        """

        bounds = self.calculate_global_bounds()
        view_box = ['{}'.format(b) for b in bounds]

        out = list()
        out.append(
            dedent(self.PREFIX)
            .replace('###VIEW_BOX###', ' '.join(view_box))
            .replace('###NAME###', self.name)
        )

        styles = []
        for entry in self.styles:
            entry_styles = []
            for name, value in entry['styles'].items():
                entry_styles.append('{}: {};'.format(name, value))
            styles.append('{} {{ {} }}'.format(
                '#{} {}'.format(self.name, entry['name']),
                ' '.join(entry_styles) ))

        if len(styles) > 0:
            styles.insert(0, self.STYLE_PREFIX)
            styles.append(self.STYLE_SUFFIX)
            out += styles

        for element in self.elements:
            ident = ''
            if element.get('name'):
                ident = 'id="{}" '.format(element['name'])

            attrs = []
            for key, value in element['attrs'].items():
                attrs.append('{}="{}"'.format(key, value))

            for key, value in element['x_attrs'].items():
                attrs.append('{}="{}"'.format(key, value))

            for key, value in element['y_attrs'].items():
                attrs.append('{}="{}"'.format(key, value))

            if element.get('data'):
                for key, value in element['data'].items():
                    attrs.append('data-{}="{}"'.format(key, value))

            if attrs:
                attrs = ' '.join(attrs) + ' '

            classes = element.get('classes')
            if classes:
                if not isinstance(classes, six.string_types):
                    classes = ' '.join(classes)
                classes = 'class="{}" '.format(classes)

            out.append('<{} {}{}{}/>'.format(
                element['tag_name'],
                ident,
                classes,
                attrs
            ))

        out.append(self.SUFFIX)
        return '\n'.join(out)

    def write(self, path):
        """

        :param path:
        :return:
        """

        with open(path, 'w+') as f:
            f.write(self.dumps())
        return self


