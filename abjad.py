import copy
import os
from xml.dom import minidom
from xml.etree import ElementTree

from shapes import Path, Circle, Group, Consonant


def create_svg(*shapes, min_x='0', min_y='0', w='75', h='75'):
    svg = ElementTree.Element(
        'svg',
        attrib={
            'viewBox': f'{min_x} {min_y} {w} {h}',
            'xmlns': 'http://www.w3.org/2000/svg'})
    for shape in shapes:
        svg.insert(1, shape.create_element())
    return svg


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


def to_file(svg, filename):
    with open(filename, 'w') as f:
        f.write(minidom.parseString(ElementTree.tostring(svg)).toprettyxml())


abjad = {
    'base_initial': Path(
        Path.M(2.5, 0),
        Path.V(57.5),
        Path.A(15, 15, 0, 0, 0, 17.5, 72.5),
        Path.H(75)),
    'base_medial': Path(
        Path.M(-12.5, 72.5),
        Path.H(75)),
    'base_medial_bar': Path(
        Path.M(2.5, 0),
        Path.V(57.5),
        Path.A(15, 15, 0, 0, 0, 17.5, 72.5),
        Path.H(75.0),
        Path.M(2.5, 57.5),
        Path.A(15, 15, 0, 0, 1, -12.5, 72.5)),
    'base_final': Path(
        Path.M(72.5, 0),
        Path.V(57.5),
        Path.A(15, 15, 0, 0, 1, 57.5, 72.5),
        Path.H(-12.5)),
    'p': Consonant(Path(
        Path.M(22.5, 55),
        Path.V(35),
        Path.A(17.5, 17.5, 0, 0, 1, 57.5, 35),
        Path.V(55))),
    'b': Consonant(Path(
        Path.M(22.5, 20),
        Path.V(40),
        Path.A(17.5, 17.5, 0, 0, 0, 57.5, 40),
        Path.V(20))),
    't': Consonant(
        Path(
            Path.M(17.5, 0),
            Path.V(55)),
        medial_bar=True, final_bar=True),
    'd': Consonant(Path(
        Path.M(20, 57.5),
        Path.H(75))),
    'k': Consonant(
        Path(
            Path.M(3.2322, 1.7678),
            Path.L(31.9822, 30.5177)),
        medial_bar=True, final_bar=True),
    'g': Consonant(Path(
        Path.M(44.4822, 43.0178),
        Path.L(73.2322, 71.7677))),
    "'": Consonant(
        Path(
            Path.M(0, 2.5),
            Path.H(30),
            Path.M(0, 27.5),
            Path.H(30)),
        medial_bar=True, final_bar=True),
    'm': Consonant(Path(
        Path.M(47.5, 72.5),
        Path.V(47.5),
        Path.H(72.5),
        Path.V(72.5))),
    'n': Consonant(Path(
        Path.M(15, 55),
        Path.H(65),
        Path.M(25, 37.5),
        Path.H(55))),
    'f': Consonant(
        Path(
            Path.M(5, 2.5),
            Path.A(22.5, 22.5, 0, 0, 1, 27.5, 25),
            Path.V(27.5),
            Path.H(0)),
        medial_bar=True, final_bar=True),
    'v': Consonant(Path(
        Path.M(72.5, 70),
        Path.A(22.5, 22.5, 0, 0, 0, 50, 47.5),
        Path.H(47.5),
        Path.V(70))),
    's': Consonant(
        Path(
            Path.M(2.5, 27.5),
            Path.H(27.5),
            Path.V(2.5),
            Path.H(2.5),
            Path.M(2.5, 2.5),
            Path.L(47.5, 47.5)),
        medial_bar=True, final_bar=True),
    'z': Consonant(Path(
        Path.M(47.5, 72.5),
        Path.V(47.5),
        Path.H(72.5),
        Path.V(72.5),
        Path.M(72.5, 72.5),
        Path.L(27.5, 27.5))),
    'x': Consonant(
        Path(
            Path.M(30, 2.5),
            Path.H(2.5),
            Path.M(2.5, 2.5),
            Path.L(47.5, 47.5)),
        medial_bar=True, final_bar=True),
    'gh': Consonant(Path(
        Path.M(72.5, 45),
        Path.V(72.5),
        Path.M(72.5, 72.5),
        Path.L(27.5, 27.5))),
    'h': Consonant(
        Path(
            Path.M(72.5, 72.5),
            Path.V(45),
            Path.A(8.2843, 8.2843, 0, 0, 0, 58.3579, 39.1421),
            Path.L(41.6421, 55.8579),
            Path.A(8.2843, 8.2843, 0, 0, 1, 27.5, 50),
            Path.V(25),
            Path.M(30.0, 2.5),
            Path.L(0, 2.5)),
        medial_bar=True, final_bar=True),
    'r': Consonant(Path(
            Path.M(12.5, 42.5),
            Path.A(20, 20, 0, 0, 0, 52.5, 42.5),
            Path.A(20, 20, 0, 0, 0, 12.5, 42.5),
            Path.M(18.3579, 56.6421),
            Path.L(46.6421, 28.3579)),
        medial_bar=True, final_bar=True, final_shift=(10, 0)),
    'l': Consonant(Path(
        Path.M(73.2322, 71.7678),
        Path.L(56.857, 55.3918),
        Path.A(15, 15, 0, 0, 0, 35.643, 55.3918),
        Path.L(19.2678, 71.7678))),
    'j': Consonant(Path(
        Path.M(72.5, 72.5),
        Path.V(52.5),
        Path.H(40),
        Path.M(57.5, 35),
        Path.H(22.5),
        Path.M(40, 17.5),
        Path.H(2.5))),
    'w': Consonant(
        Path(
            Path.M(12.5, 50),
            Path.A(12.5, 12.5, 0, 0, 0, 37.5, 50),
            Path.A(12.5, 12.5, 0, 0, 0, 12.5, 50)),
        medial_bar=True, final_bar=True),
    'e': Path(
        Path.M(56.75, 18.25),
        Path.L(73.25, 1.75)),
    'i': Path(
        Path.M(57.5, 0),
        Path.V(17.5),
        Path.H(75)),
    'u': Path(
        Path.M(55, 2.5),
        Path.A(17.5, 17.5, 0, 0, 1, 72.5, 20)),
    'o': Path(
        Path.M(56.75, 18.25),
        Path.L(73.25, 1.75),
        Path.M(56.75, 1.75),
        Path.L(73.25, 18.25)),
    'y': Group(
        Circle('58.5', '3.5', '3.5'),
        Circle('71.5', '16.5', '3.5')),
    'ø': Path(
        Path.M(57.5, 10),
        Path.A(7.5, 7.5, 0, 0, 0, 72.5, 10),
        Path.A(7.5, 7.5, 0, 0, 0, 57.5, 10)),
    '0': Path(
        Path.M(37.5, 2.5),
        Path.H(17.5),
        Path.A(15, 15, 0, 0, 0, 2.5, 17.5),
        Path.V(57.5),
        Path.A(15, 15, 0, 0, 0, 17.5, 72.5),
        Path.H(57.5),
        Path.A(15, 15, 0, 0, 0, 72.5, 57.5),
        Path.V(17.5),
        Path.A(15, 15, 0, 0, 0, 57.5, 2.5),
        Path.H(37.5)),
    '1': Path(
        Path.M(10, 37.5),
        Path.H(65)),
    '2': Path(
        Path.M(10, 37.5),
        Path.H(65),
        Path.M(37.5, 10),
        Path.V(65)),
    '3': Path(
        Path.M(10, 37.5),
        Path.H(65),
        Path.M(25, 20),
        Path.H(50),
        Path.M(25, 55),
        Path.H(50)),
    '4': Path(
        Path.M(25.376, 55),
        Path.H(49.624),
        Path.A(7, 7, 0, 0, 0, 55.687, 44.5),
        Path.L(43.562, 23.5),
        Path.A(7, 7, 0, 0, 0, 31.438, 23.5),
        Path.L(19.313, 44.5),
        Path.A(7, 7, 0, 0, 0, 25.376, 55),
        Path.Z()),
    '5': Path(
        Path.M(20, 25.376),
        Path.V(49.624),
        Path.A(7, 7, 0, 0, 0, 30.5, 55.687),
        Path.L(51.5, 43.562),
        Path.A(7, 7, 0, 0, 0, 51.5, 31.438),
        Path.L(30.5, 19.313),
        Path.A(7, 7, 0, 0, 0, 20, 25.376),
        Path.M(30.5, 55.687),
        Path.V(19.313)),
    '6': Path(
        Path.M(25.376, 25),
        Path.H(49.624),
        Path.A(7, 7, 0, 0, 1, 55.687, 35.5),
        Path.L(43.562, 56.5),
        Path.A(7, 7, 0, 0, 1, 31.438, 56.5),
        Path.L(19.313, 35.5),
        Path.A(7, 7, 0, 0, 1, 25.376, 25),
        Path.M(25.376, 15),
        Path.H(49.624)),
    '7': Path(
        Path.M(37.5, 2.5),
        Path.A(35, 35, 0, 0, 1, 2.5, 37.5)),
    '8': Path(
        Path.M(37.5, 2.5),
        Path.A(35, 35, 0, 0, 1, 2.5, 37.5),
        Path.M(37.5, 72.5),
        Path.A(35, 35, 0, 0, 1, 72.5, 37.5)),
    '9': Path(
        Path.M(37.5, 2.5),
        Path.A(35, 35, 0, 0, 0, 72.5, 37.5),
        Path.M(37.5, 72.5),
        Path.A(35, 35, 0, 0, 0, 2.5, 37.5),
        Path.M(47.751, 27.249),
        Path.L(27.249, 47.751))}


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
