import copy
import os
from xml.dom import minidom
from xml.etree import ElementTree


def create_svg(*shapes, min_x='0', min_y='0', w='75', h='75'):
    svg = ElementTree.Element(
        'svg',
        attrib={
            'viewBox': f'{min_x} {min_y} {w} {h}',
            'xmlns': 'http://www.w3.org/2000/svg'})
    for shape in shapes:
        svg.insert(1, shape.create_element())
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


def to_file(svg, filename):
    with open(filename, 'w') as f:
        f.write(minidom.parseString(ElementTree.tostring(svg)).toprettyxml())


def create_initial_svg(consonant, *vowel):
    return create_svg(abjad['base_initial'], consonant.shape, *vowel)


def create_medial_svg(consonant, *vowel):
    if consonant.medial_bar:
        return create_svg(
            abjad['base_medial_bar'], consonant.shape, *vowel,
            min_x='-12.5', w='87.5')
    else:
        return create_svg(abjad['base_medial'], consonant.shape, *vowel)


def create_final_svg(consonant):
    if consonant.final_bar:
        new_shape = copy.deepcopy(consonant.shape)
        # TODO not removing overlap properly when loading,
        #  flip coords without transform
        try:
            x, y = consonant.final_shift
            new_shape.attrib.update({'transform': f'translate({x} {y})'})
        except TypeError:
            new_shape.attrib.update(
                {'transform': 'scale(-1 1) translate(-75 0)'})
        return create_svg(abjad['base_final'], new_shape)
    return create_medial_svg(consonant)


abjad = {
    'base_initial': Path(
        'M 2.5 0 '
        'V 57.5 '
        'A 15 15 0 0 0 17.5 72.5 '
        'H 75.0'),
    'base_medial': Path(
        'M -12.5 72.5 '
        'H 75'),
    'base_medial_bar': Path(
        'M 2.5 0 '
        'V 57.5 '
        'A 15 15 0 0 0 17.5 72.5 '
        'H 75.0 '
        'M 2.5 57.5 '
        'A 15 15 0 0 1 -12.5 72.5'),
    'base_final': Path(
        'M 72.5 0 '
        'V 57.5 '
        'A 15 15 0 0 1 57.5 72.5 '
        'H -12.5'),
    'p': Consonant(Path(
        'M 22.5 55 '
        'V 35 '
        'A 17.5 17.5 0 0 1 57.5 35 '
        'V 55')),
    'b': Consonant(Path(
        'M 22.5 20 '
        'V 40 '
        'A 17.5 17.5 0 0 0 57.5 40 '
        'V 20')),
    't': Consonant(
        Path(
            'M 17.5 0 '
            'V 55'),
        medial_bar=True, final_bar=True),
    'd': Consonant(Path(
        'M 20.0 57.5 '
        'H 75.0')),
    'k': Consonant(
        Path(
            'M 3.2322 1.7678 '
            'L 31.9822 30.5177'),
        medial_bar=True, final_bar=True),
    'g': Consonant(Path(
        'M 44.4822 43.0178 '
        'L 73.2322 71.7677 ')),
    "'": Consonant(
        Path(
            'M 0.0 2.5 '
            'H 30.0 '
            'M 0.0 27.5 '
            'H 30.0'),
        medial_bar=True, final_bar=True),
    'm': Consonant(Path(
        'M 47.5 72.5 '
        'V 47.5 '
        'H 72.5 '
        'V 72.5')),
    'n': Consonant(Path(
        'M 15.0 55 '
        'H 65.0 '
        'M 25.0 37.5 '
        'H 55.0')),
    'f': Consonant(
        Path(
            'M 5.0 2.5 '
            'A 22.5 22.5 0 0 1 27.5 25 '
            'V 27.5 '
            'H 0.0'),
        medial_bar=True, final_bar=True),
    'v': Consonant(Path(
        'M 72.5 70 '
        'A 22.5 22.5 0 0 0 50.0 47.5 '
        'H 47.5 '
        'V 70')),
    's': Consonant(
        Path(
            'M 2.5 27.5 '
            'H 27.5 '
            'V 2.5 '
            'H 2.5 '
            'M 2.5 2.5 '
            'L 47.5 47.5'),
        medial_bar=True, final_bar=True),
    'z': Consonant(Path(
        'M 47.5 72.5 '
        'V 47.5 '
        'H 72.5 '
        'V 72.5 '
        'M 72.5 72.5 '
        'L 27.5 27.5')),
    'x': Consonant(
        Path(
            'M 30.0 2.5 '
            'H 2.5 '
            'M 2.5 2.5 '
            'L 47.5 47.5'),
        medial_bar=True, final_bar=True),
    'gh': Consonant(Path(
        'M 72.5 45 '
        'V 72.5 '
        'M 72.5 72.5 '
        'L 27.5 27.5')),
    'h': Consonant(
        Path(
            'M 72.5 72.5 '
            'V 45 '
            'A 8.2843 8.2843 0 0 0 58.3579 39.1421 '
            'L 41.6421 55.8579 '
            'A 8.2843 8.2843 0 0 1 27.5 50 '
            'V 25 '
            'M 30.0 2.5 '
            'L 0.0 2.5'),
        medial_bar=True, final_bar=True),
    'r': Consonant(Path(
        'M 12.5 42.5 '
        'A 20 20 0 0 0 52.5 42.5 '
        'A 20 20 0 0 0 12.5 42.5 '
        'M 18.3579 56.6421 '
        'L 46.6421 28.3579'),
        medial_bar=True, final_bar=True, final_shift=(10, 0)),
    'l': Consonant(Path(
        'M 73.2322 71.7678 '
        'L 56.857 55.3918 '
        'A 15 15 0 0 0 35.643 55.3918 '
        'L 19.2678 71.7678')),
    'j': Consonant(Path(
        'M 72.5 72.5 '
        'V 52.5 '
        'H 40.0 '
        'M 57.5 35 '
        'H 22.5 '
        'M 40.0 17.5 '
        'H 2.5')),
    'w': Consonant(
        Path(
            'M 12.5 50 '
            'A 12.5 12.5 0 0 0 37.5 50 '
            'A 12.5 12.5 0 0 0 12.5 50'),
        medial_bar=True, final_bar=True),
    'e': Path(
        'M 56.75 18.25 '
        'L 73.25 1.75 '),
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
        'L 27.249 47.751')}


def create_all_glyphs():
    numerals = [
        '0', '1', '2', '3', '4',
        '5', '6', '7', '8', '9']
    consonants = [
        'p', 'b', 'm', 'f', 'v',
        't', 'd', 'n', 's', 'z',
        'k', 'g', 'x', 'gh', "'",
        'h', 'r', 'l', 'j', 'w']
    vowels = [
        'e', 'i', 'u', 'o', 'y', 'ø']

    subdir = 'abjad_svg'
    if not os.path.isdir(subdir):
        os.mkdir(subdir)

    i = 0
    for numeral in numerals:
        parts = ('0',)
        if numeral != '0':
            parts = parts + (numeral,)
        to_file(
            create_svg(*(abjad[part] for part in parts)),
            os.path.join(subdir, f'{i}_{numeral}.svg'))
        i += 1
    to_file(create_svg(), os.path.join(subdir, f'{i}_SPACE.svg'))
    i += 1
    for consonant in consonants:
        to_file(
            create_initial_svg(abjad[consonant]),
            os.path.join(subdir, f'{i}_{consonant.upper()}.svg'))
        i += 1
        to_file(
            create_medial_svg(abjad[consonant]),
            os.path.join(subdir, f'{i}_{consonant.upper()}.medial.svg'))
        i += 1
        to_file(
            create_final_svg(abjad[consonant]),
            os.path.join(subdir, f'{i}_{consonant.upper()}.final.svg'))
        i += 1
        for vowel in vowels:
            to_file(
                create_initial_svg(abjad[consonant], abjad[vowel]),
                os.path.join(
                    subdir,
                    f'{i}_{consonant.upper()}.{vowel.upper()}.svg'))
            i += 1
            to_file(
                create_medial_svg(abjad[consonant], abjad[vowel]),
                os.path.join(
                    subdir,
                    f'{i}_{consonant.upper()}.{vowel.upper()}.medial.svg'))
            i += 1
    for vowel in vowels:
        to_file(
            create_svg(abjad[vowel], min_x='55', w='20'),
            os.path.join(subdir, f'{i}_{vowel.upper()}.svg'))
        i += 1


if __name__ == '__main__':
    create_all_glyphs()
