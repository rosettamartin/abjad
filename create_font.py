import os

import fontforge

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

path = os.path.dirname(__file__)
svg_path = os.path.join(path, 'abugida_svg')
new_font = fontforge.font()
new_font.ascent = 1000
new_font.descent = 0
new_font.encoding = 'UnicodeFull'
i = 0
code_point = 57344
for numeral in numerals:
    filename = os.path.join(svg_path, f'{i}_{numeral}.svg')
    i += 1
    code_point += 1
    glyph = new_font.createChar(code_point)
    glyph.right_side_bearing = 1067
    glyph.importOutlines(filename)
filename = os.path.join(svg_path, f'{i}_null.svg')
i += 1
code_point += 1
glyph = new_font.createChar(code_point)
glyph.width = 250
glyph.right_side_bearing = 250 + 67
glyph.importOutlines(filename)
for consonant in consonants:
    for vowel in vowels:
        filename = os.path.join(svg_path, f'{i}_{consonant}{vowel}.svg')
        i += 1
        code_point += 1
        glyph = new_font.createChar(code_point)
        glyph.right_side_bearing = 1067
        glyph.importOutlines(filename)

new_font.encoding = 'compacted'

font_filename = 'testfont.ttf'
new_font.fontname = "testfont"
new_font.save(os.path.join(path, font_filename))
