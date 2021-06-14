import os

import fontforge

numerals = [
    '0', '1', '2', '3', '4',
    '5', '6', '7', '8', '9']
numeral_strings = [
    'ZERO', 'ONE', 'TWO', 'THREE', 'FOUR',
    'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE']
consonants = [
    'p', 'b', 'm', 'f', 'v',
    't', 'd', 'n', 's', 'z',
    'k', 'g', 'x', 'gh', "'",
    'h', 'r', 'l', 'j', 'w']
vowels = [
    'e', 'i', 'u', 'o', 'y', 'ø']

path = os.path.dirname(__file__)
svg_path = os.path.join(path, 'abugida_svg')

new_font = fontforge.font()
new_font.ascent = 1000
new_font.descent = 0
new_font.encoding = 'UnicodeFull'
new_font.addLookup(
    'Composition Lookup',
    'gsub_ligature',
    None,
    (('ccmp', (('dflt', ('dflt',)),)),))
new_font.addLookupSubtable('Composition Lookup', 'Compositions')

i = 0
code_point = 57344
for numeral, numeral_string in zip(numerals, numeral_strings):
    filename = os.path.join(svg_path, f'{i}_{numeral}.svg')
    i += 1
    code_point += 1
    glyph = new_font.createChar(code_point, f'conlang{numeral_string}')
    glyph.right_side_bearing = 1067
    glyph.importOutlines(filename)
filename = os.path.join(svg_path, f'{i}_null.svg')
i += 1
code_point += 1
glyph = new_font.createChar(code_point, 'conlangNULL')
glyph.width = 250
glyph.right_side_bearing = 250 + 67
glyph.importOutlines(filename)
for consonant in consonants:
    for vowel in vowels:
        filename = os.path.join(svg_path, f'{i}_{consonant}{vowel}.svg')
        i += 1
        code_point += 1
        glyph = new_font.createChar(
            code_point, f'conlang{consonant.upper()}{vowel.upper()}')
        if vowel != 'e':
            glyph.addPosSub(
                'Compositions', (
                    f'conlang{consonant.upper()}E',
                    f'conlang{vowel.upper()}'))
        glyph.right_side_bearing = 1067
        glyph.importOutlines(filename)
for vowel in vowels:
    if vowel != 'e':
        filename = os.path.join(svg_path, f'{i}_{vowel}.svg')
        i += 1
        code_point += 1
        glyph = new_font.createChar(code_point, f'conlang{vowel.upper()}')
        glyph.importOutlines(filename)

new_font.encoding = 'compacted'

new_font.selection.all()
new_font.removeOverlap()
new_font.correctDirection()
new_font.addExtrema()
new_font.round()

font_filename = 'testfont'
new_font.fontname = "testfont"
new_font.save(os.path.join(path, font_filename + '.sfd'))
new_font.generate(os.path.join(path, font_filename + '.ttf'))
