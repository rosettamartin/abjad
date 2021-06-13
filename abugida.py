from xml.dom import minidom
from xml.etree import ElementTree


class Abugida:
    def __init__(self, letters):
        self.letters = letters

    def create_svg(self, letters):
        svg = ElementTree.Element(
            'svg',
            attrib={
                'viewBox': '0 0 85 85',
                'xmlns': 'http://www.w3.org/2000/svg'})
        for letter in letters:
            svg.insert(1, ElementTree.Element(
                'path',
                attrib={
                    'd': self.letters[letter],
                    'stroke': 'black',
                    'fill': 'none',
                    'stroke-width': '5px'}))
        return svg


def to_file(svg, filename):
    with open(filename, 'w') as f:
        f.write(minidom.parseString(ElementTree.tostring(svg)).toprettyxml())


abugida = Abugida({
    'base':
        'M 12.5 0 '
        'V 57.5 '
        'A 15 15 0 0 0 27.5 72.5 '
        'H 85',
    'p':
        'M 32.5 55 '
        'V 35 '
        'A 17.5 17.5 0 0 1 67.5 35 '
        'V 55',
    'b':
        'M 32.5 20 '
        'V 40 '
        'A 17.5 17.5 0 0 0 67.5 40 '
        'V 20',
    't':
        'M 27.5 0 '
        'V 55',
    'd':
        'M 30 57.5 '
        'H 85',
    'k':
        'M 36.75 23.25 '
        'L 12.5 0 '
        'M 12.5 10',
    'g':
        'M 56.75 43.25 '
        'L 85 72.5 '
        'M 60 72.5',
    "'":
        'M 10 2.5 '
        'H 40 '
        'M 10 27.5 '
        'H 40',
    'm':
        'M 57.5 72.5  '
        'V 47.5 '
        'H 82.5 '
        'V 72.5',
    'n':
        'M 25 55 '
        'H 75 '
        'M 35 37.5 '
        'H 65',
    'f':
        'M 15 2.5 '
        'A 22.5 22.5 0 0 1 37.5 25 '
        'V 27.5 '
        'H 10',
    'v':
        'M 82.5 70 '
        'A 22.5 22.5 0 0 0 60 47.5 '
        'H 57.5 '
        'V 70',
    's':
        'M 12.5 27.5 '
        'H 37.5 '
        'V 2.5 '
        'H 12.5 '
        'M 12.5 2.5 '
        'L 57.5 47.5',
    'z':
        'M 57.5 72.5  '
        'V 47.5 '
        'H 82.5 '
        'V 72.5 '
        'M 82.5 72.5 '
        'L 37.5 27.5',
    'x':
        'M 40 2.5 '
        'H 12.5 '
        'M 12.5 2.5 '
        'L 57.5 47.5',
    'gh':
        'M 82.5 45 '
        'V 72.5 '
        'M 82.5 72.5 '
        'L 37.5 27.5',
    'h':
        'M 82.5 72.5 '
        'V 45 '
        'A 8.2843 8.2843 0 0 0 68.3579 39.1421 '
        'L 51.6421 55.8579 '
        'A 8.2843 8.2843 0 0 1 37.5 50 '
        'V 25 '
        'M 40 2.5 '
        'L 10 2.5',
    'r':
        'M 22.5 42.5 '
        'A 20 20 0 0 0 62.5 42.5 '
        'A 20 20 0 0 0 22.5 42.5 '
        'M 28.3579 56.6421 '
        'L 56.6421 28.3579',
    'l':
        'M 12.5 0 '
        'L 30.6434 18.1434 '
        'A 15 15 0 0 1 30.6434 39.3566 '
        'L 12.5 57.5',
    'j':
        'M 82.5 72.5 '
        'V 52.5 '
        'H 50 '
        'M 67.5 35 '
        'H 32.5 '
        'M 50 17.5 '
        'H 12.5',
    'w':
        'M 22.5 50 '
        'A 12.5 12.5 0 0 0 47.5 50 '
        'A 12.5 12.5 0 0 0 22.5 50',
    'i':
        'M 67.5 0 '
        'V 17.5 '
        'H 85',
    'u':
        'M 65 2.5 '
        'A 17.5 17.5 0 0 1 82.5 20',
    'o':
        'M 66.75 18.25 '
        'L 83.25 1.75 '
        'M 66.75 1.75 '
        'L 83.25 18.25',
    'y':
        'M 2.5 0 '
        'V 20',
    'ø':
        'M 65 82.5 '
        'H 85'})

if __name__ == '__main__':
    to_file(abugida.create_svg(('base', 'h', 'y')), 'svg/d1.svg')
    to_file(abugida.create_svg(('base', 'w', 'y2')), 'svg/d2.svg')
    to_file(abugida.create_svg(('base', 'h', 'ø')), 'svg/d3.svg')
    to_file(abugida.create_svg(('base', 'w', 'ø2')), 'svg/d4.svg')
    to_file(abugida.create_svg(('base', 'w', 'ø3')), 'svg/d5.svg')

    # to_file(abugida.create_svg(('base', 'w', 'y2')), 'svg/2.svg')
