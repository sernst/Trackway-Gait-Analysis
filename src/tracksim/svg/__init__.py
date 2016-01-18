from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import random
from textwrap import dedent

import six
import tracksim

class SvgWriter(object):

    PREFIX = """
    <svg version="1.1"
        id="###NAME###",
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="###VIEW_BOX###">
    """

    SUFFIX = "</svg>"

    STYLE_PREFIX = '<style>\n/* <![CDATA[ */'
    STYLE_SUFFIX = '/* ]]> */\n</style>'

    LIMB_COLORS = tracksim.LimbProperty(
        left_pes='DodgerBlue',
        right_pes='DarkOrange',
        left_manus='DarkOliveGreen',
        right_manus='DarkOrchid' )

    def __init__(self):
        self.padding = 20
        self.scale = 1.0
        self.offset = (0, 0)
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


    def draw_circle(self, x, y, radius, classes, name = None):
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
            classes=classes)

    def set_offset(self, x = None, y = None):
        """

        :param x:
        :param y:
        :return:
        """

        self.offset = (
            self.offset[0] + (0 if x is None else x),
            self.offset[1] + (0 if y is None else y) )

        for element in self.elements:
            bounds = element.get('bounds')
            if x is not None:
                if bounds:
                    bounds[0] += x
                    bounds[2] += x
                for key, value in element['x_attrs'].items():
                    element['x_attrs'][key] += x

            if y is not None:
                bounds[1] += y
                bounds[3] += y
                for key, value in element['y_attrs'].items():
                    element['y_attrs'][key] += x

    def add_element(self, **kwargs):
        self.elements.append(kwargs)

    def dumps(self):
        """

        :return:
        """

        bounds = [0, 0, 0, 0]
        for element in self.elements:
            element_bounds = element.get('bounds')
            if element_bounds:
                bounds[0] = math.floor(min(element_bounds[0], bounds[0]))
                bounds[1] = math.floor(min(element_bounds[1], bounds[1]))
                bounds[2] = math.ceil(max(element_bounds[2], bounds[2]))
                bounds[3] = math.ceil(max(element_bounds[3], bounds[3]))

        bounds[0] -= self.padding
        bounds[1] -= self.padding
        bounds[2] += self.padding - bounds[0]
        bounds[3] += self.padding - bounds[1]
        bounds = [str(b) for b in bounds]

        out = list()
        out.append(
            dedent(self.PREFIX)
                .replace('###VIEW_BOX###', ' '.join(bounds))
                .replace('###NAME###', self.name) )

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
                attrs ))

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


