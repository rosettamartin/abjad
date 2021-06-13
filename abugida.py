from xml.dom import minidom
from xml.etree import ElementTree


class Abugida:
    def __init__(self, letters):
        self.letters = letters

    def create_svg(self, letters, w='75', h='75'):
        svg = ElementTree.Element(
            'svg',
            attrib={
                'viewBox': f'0 0 {w} {h}',
                'xmlns': 'http://www.w3.org/2000/svg'})
        for letter in letters:
            svg.insert(1, self.letters[letter].create_element())
        return svg


class Path:
    def __init__(self, d, **attrib):
        self.d = d
        self.attrib = {
            'stroke': 'black',
            'fill': 'none',
            'stroke-width': '5px',
            **attrib}

    def create_element(self):
        return ElementTree.Element(
            'path',
            attrib={
                'd': self.d,
                **self.attrib})


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


def to_file(svg, filename):
    with open(filename, 'w') as f:
        f.write(minidom.parseString(ElementTree.tostring(svg)).toprettyxml())


abugida = Abugida({
    'null': Path(
        'M 0 2.5 '
        'H 16.25 '
        'V 57.5 '
        'A 15 15 0 0 1 1.25 72.5 '
        'H 0'),
    'base': Path(
        'M 2.5 0 '
        'V 57.5 '
        'A 15 15 0 0 0 17.5 72.5 '
        'H 75.0'),
    'p': Path(
        'M 22.5 55 '
        'V 35 '
        'A 17.5 17.5 0 0 1 57.5 35 '
        'V 55'),
    'b': Path(
        'M 22.5 20 '
        'V 40 '
        'A 17.5 17.5 0 0 0 57.5 40 '
        'V 20'),
    't': Path(
        'M 17.5 0 '
        'V 55'),
    'd': Path(
        'M 20.0 57.5 '
        'H 75.0'),
    'k': Path(
        'M 3.2322 1.7678 '
        'L 31.9822 30.5177'),
    'g': Path(
        'M 44.4822 43.0178 '
        'L 73.2322 71.7677 '),
    "'": Path(
        'M 0.0 2.5 '
        'H 30.0 '
        'M 0.0 27.5 '
        'H 30.0'),
    'm': Path(
        'M 47.5 72.5 '
        'V 47.5 '
        'H 72.5 '
        'V 72.5'),
    'n': Path(
        'M 15.0 55 '
        'H 65.0 '
        'M 25.0 37.5 '
        'H 55.0'),
    'f': Path(
        'M 5.0 2.5 '
        'A 22.5 22.5 0 0 1 27.5 25 '
        'V 27.5 '
        'H 0.0'),
    'v': Path(
        'M 72.5 70 '
        'A 22.5 22.5 0 0 0 50.0 47.5 '
        'H 47.5 '
        'V 70'),
    's': Path(
        'M 2.5 27.5 '
        'H 27.5 '
        'V 2.5 '
        'H 2.5 '
        'M 2.5 2.5 '
        'L 47.5 47.5'),
    'z': Path(
        'M 47.5 72.5 '
        'V 47.5 '
        'H 72.5 '
        'V 72.5 '
        'M 72.5 72.5 '
        'L 27.5 27.5'),
    'x': Path(
        'M 30.0 2.5 '
        'H 2.5 '
        'M 2.5 2.5 '
        'L 47.5 47.5'),
    'gh': Path(
        'M 72.5 45 '
        'V 72.5 '
        'M 72.5 72.5 '
        'L 27.5 27.5'),
    'h': Path(
        'M 72.5 72.5 '
        'V 45 '
        'A 8.2843 8.2843 0 0 0 58.3579 39.1421 '
        'L 41.6421 55.8579 '
        'A 8.2843 8.2843 0 0 1 27.5 50 '
        'V 25 '
        'M 30.0 2.5 '
        'L 0.0 2.5'),
    'r': Path(
        'M 12.5 42.5 '
        'A 20 20 0 0 0 52.5 42.5 '
        'A 20 20 0 0 0 12.5 42.5 '
        'M 18.3579 56.6421 '
        'L 46.6421 28.3579'),
    'l': Path(
        'M 3.2322 1.7678 '
        'L 19.6082 18.143 '
        'A 15 15 0 0 1 19.6082 39.357 '
        'L 3.2322 55.7322'),
    'j': Path(
        'M 72.5 72.5 '
        'V 52.5 '
        'H 40.0 '
        'M 57.5 35 '
        'H 22.5 '
        'M 40.0 17.5 '
        'H 2.5'),
    'w': Path(
        'M 12.5 50 '
        'A 12.5 12.5 0 0 0 37.5 50 '
        'A 12.5 12.5 0 0 0 12.5 50'),
    'i': Path(
        'M 57.5 0 '
        'V 17.5 '
        'H 75.0'),
    'u': Path(
        'M 55.0 2.5 '
        'A 17.5 17.5 0 0 1 72.5 20'),
    'o': Path(
        'M 56.75 18.25 '
        'L 73.25 1.75 '
        'M 56.75 1.75 '
        'L 73.25 18.25'),
    'y': Group(
        Circle('58.5', '3.5', '3.5'),
        Circle('71.5', '16.5', '3.5')),
    'ø': Path(
        'M 57.5 10 '
        'A 7.5 7.5 0 0 0 72.5 10 '
        'A 7.5 7.5 0 0 0 57.5 10'),
    '0': Path(
        'M 37.5 2.5 '
        'H 17.5 '
        'A 15 15 0 0 0 2.5 17.5 '
        'V 57.5 '
        'A 15 15 0 0 0 17.5 72.5 '
        'H 57.5 '
        'A 15 15 0 0 0 72.5 57.5 '
        'V 17.5 '
        'A 15 15 0 0 0 57.5 2.5 '
        'H 37.5'),
    '1': Path(
        'M 10 37.5 '
        'H 65'),
    '2': Path(
        'M 10 37.5 '
        'H 65 '
        'M 37.5 10 '
        'V 65'),
    '3': Path(
        'M 10 37.5 '
        'H 65 '
        'M 25 20 '
        'H 50 '
        'M 25 55 '
        'H 50'),
    '4': Path(
        'M 25.376 55 '
        'H 49.624 '
        'A 7 7 0 0 0 55.687 44.5 '
        'L 43.562 23.5 '
        'A 7 7 0 0 0 31.438 23.5 '
        'L 19.313 44.5 '
        'A 7 7 0 0 0 25.376 55 '
        'Z'),
    '5': Path(
        'M 20 25.376 '
        'V 49.624 '
        'A 7 7 0 0 0 30.5 55.687 '
        'L 51.5 43.562 '
        'A 7 7 0 0 0 51.5 31.438 '
        'L 30.5 19.313 '
        'A 7 7 0 0 0 20 25.376 '
        'M 30.5 55.687 '
        'V 19.313'),
    '6': Path(
        'M 25.376 25 '
        'H 49.624 '
        'A 7 7 0 0 1 55.687 35.5 '
        'L 43.562 56.5 '
        'A 7 7 0 0 1 31.438 56.5 '
        'L 19.313 35.5 '
        'A 7 7 0 0 1 25.376 25 '
        'M 25.376 15 '
        'H 49.624'),
    '7': Path(
        'M 37.5 2.5 '
        'A 35 35 0 0 1 2.5 37.5'),
    '8': Path(
        'M 37.5 2.5 '
        'A 35 35 0 0 1 2.5 37.5 '
        'M 37.5 72.5 '
        'A 35 35 0 0 1 72.5 37.5'),
    '9': Path(
        'M 37.5 2.5 '
        'A 35 35 0 0 0 72.5 37.5 '
        'M 37.5 72.5 '
        'A 35 35 0 0 0 2.5 37.5 '
        'M 47.751 27.249 '
        'L 27.249 47.751')
})

if __name__ == '__main__':
    to_file(abugida.create_svg(('base', 'h', 'y')), 'svg/d1.svg')
    to_file(abugida.create_svg(('base', 'h', 'ø')), 'svg/d3.svg')

    # to_file(abugida.create_svg(('base', 'w', 'y2')), 'svg/2.svg')
