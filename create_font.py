import os

import fontforge

path = os.path.dirname(__file__)
svg_path = os.path.join(path, 'abjad_svg')

new_font = fontforge.font()
new_font.ascent = 1000
new_font.descent = 0
new_font.encoding = 'UnicodeFull'

letters = []
new_font.addLookup(
    'Composition Lookup',
    'gsub_ligature',
    None,
    (('ccmp', (('dflt', ('dflt',)),)),))
new_font.addLookupSubtable('Composition Lookup', 'Compositions')
new_font.addLookup(
    'Medial',
    'gsub_single',
    None,
    (('medi', (('dflt', ('dflt',)),)),))
new_font.addLookupSubtable('Medial', 'Medial Forms')
new_font.addLookup(
    'Final',
    'gsub_single',
    None,
    (('fina', (('dflt', ('dflt',)),)),))
new_font.addLookupSubtable('Final', 'Final Forms')
new_font.addLookup(
    'Contextual Alternates',
    'gsub_contextchain',
    None,
    (('calt', (('dflt', ('dflt',)),)),))

code_point = 57344

files = sorted(os.listdir(svg_path), key=lambda x: int(x.split('_')[0]))
char_names = [file.split('_')[-1].replace('.svg', '') for file in files]
for i, file, char_name in zip(range(len(files)), files, char_names):
    glyph_name = f'conlang{char_name}'
    if char_name == 'SPACE':
        # U+2003 Em Space
        glyph = new_font.createChar(8195, glyph_name)
    elif '.' in char_name:
        glyph = new_font.createChar(-1, glyph_name)
        # if not char_name.endswith(('.medial', '.final')):
        #     consonant, vowel = char_name.split('.')
        #     glyph.addPosSub(
        #         'Compositions', (f'conlang{consonant}', f'conlang{vowel}'))
    else:
        glyph = new_font.createChar(code_point, glyph_name)
        code_point += 1

    if not char_name.isnumeric() and not char_name == 'SPACE':
        letters.append(glyph_name)
        if not char_name.endswith(('.medial', '.final')):
            if char_name + '.medial' in char_names:
                glyph.addPosSub('Medial Forms', glyph_name + '.medial')
            if char_name + '.final' in char_names:
                glyph.addPosSub('Final Forms', glyph_name + '.final')

    for vowel in ['E', 'I', 'U', 'O', 'Y', 'Ø']:
        if vowel in char_name:
            glyph.addPosSub(
                'Compositions',
                (glyph_name.replace('.' + vowel, ''), f'conlang{vowel}'))

    glyph.importOutlines(os.path.join(svg_path, file))
    glyph.left_side_bearing = 0
    if char_name.isnumeric():
        glyph.right_side_bearing = 67
    elif char_name == 'SPACE':
        glyph.right_side_bearing = 1000
    else:
        glyph.right_side_bearing = 0

classes = (None, letters)
new_font.addContextualSubtable(
    lookup='Contextual Alternates',
    subtable='Final Alternate Rule',
    type='class',
    rule=' 1 | 1 @<Final> | ',
    bclasses=classes,
    mclasses=classes,
    fclasses=classes)
new_font.addContextualSubtable(
    lookup='Contextual Alternates',
    subtable='Medial Alternate Rule',
    type='class',
    rule=' 1 | 1 @<Medial> | 1 ',
    bclasses=classes,
    mclasses=classes,
    fclasses=classes)

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
