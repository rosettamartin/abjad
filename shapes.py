import copy
from xml.etree import ElementTree


class Path:
    class M:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def to_string(self):
            return f'M {self.x} {self.y}'

    class L:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def to_string(self):
            return f'L {self.x} {self.y}'

    class H:
        def __init__(self, x):
            self.x = x

        def to_string(self):
            return f'H {self.x}'

    class V:
        def __init__(self, y):
            self.y = y

        def to_string(self):
            return f'V {self.y}'

    class A:
        def __init__(self,
                     rx, ry, x_axis_rotation, large_arc_flag, sweep_flag,
                     x, y):
            self.rx, self.ry, self.x, self.y = rx, ry, x, y
            self.x_axis_rotation = x_axis_rotation
            self.large_arc_flag = large_arc_flag
            self.sweep_flag = sweep_flag

        def to_string(self):
            return (
                f'A {self.rx} {self.ry} '
                f'{self.x_axis_rotation} {self.large_arc_flag} '
                f'{self.sweep_flag} '
                f'{self.x} {self.y}')

    class Z:
        @staticmethod
        def to_string():
            return 'Z'

    def __init__(self, *commands, **attrib):
        self.commands = commands
        self.attrib = {
            'stroke': 'black',
            'fill': 'none',
            'stroke-width': '5px',
            **attrib}

    def create_element(self):
        return ElementTree.Element(
            'path',
            attrib={
                'd': ' '.join([
                    command.to_string() for command in self.commands]),
                **self.attrib})

    def flipped_horizontal(self, across):
        """
        Return a copy of this Path flipped horizontally across the point
        `across`.

        :param across: A numeric x value
        :return: The flipped Path
        """

        new_path = copy.deepcopy(self)
        for command in new_path.commands:
            try:
                command.x = (2 * across) - command.x
            except AttributeError:
                pass
            try:
                command.sweep_flag = 1 - command.sweep_flag
            except AttributeError:
                pass
        return new_path

    def translate(self, x, y):
        """
        Return a copy of this Path with its `x` and `y` values
        translated by `x` and `y` respectively.

        :param x: A numeric x value
        :param y: A numeric y value
        :return: The moved Path
        """

        new_path = copy.deepcopy(self)
        for command in new_path.commands:
            try:
                command.x += x
            except AttributeError:
                pass
            try:
                command.y += y
            except AttributeError:
                pass
        return new_path


class Circle:
    def __init__(self, cx, cy, r, **attrib):
        self.cx, self.cy, self.r = cx, cy, r
        self.attrib = attrib

    def create_element(self):
        return ElementTree.Element(
            'circle',
            attrib={
                'cx': self.cx,
                'cy': self.cy,
                'r': self.r,
                **self.attrib})


class Group:
    def __init__(self, *items, **attrib):
        self.items = items
        self.attrib = attrib

    def create_element(self):
        element = ElementTree.Element('g', attrib=self.attrib)
        for item in self.items:
            element.insert(1, item.create_element())
        return element


class Consonant:
    def __init__(self, shape,
                 medial_bar=False, final_bar=False, final_shift=None):
        """
        A consonant character. `shape` is either a Path, Circle, or
        Group. The boolean value `medial_bar` specifies whether the
        consonant's base shape requires a vertical bar. The boolean
        value `final_bar` specifies whether the consonant's final form
        requires a vertical bar. `final_shift` is a 2-tuple of x and y
        values; if provided, the consonant's final form will be shifted
        by x and y, rather than flipped horizontally.

        :param shape: A Path, Circle, or Group
        :param medial_bar: A boolean
        :param final_bar: A boolean
        :param final_shift: a 2-tuple of x and y values
        """

        self.shape = shape
        self.medial_bar = medial_bar
        self.final_bar = final_bar
        self.final_shift = final_shift
