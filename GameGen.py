#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Master Game Gen
1.0b
'''
import os
import sys
import json

from OS_Helper import CleanDirectory, BuildPage, BuildBack

#TSSSF Migration TODO:
#automagickally create vassal module :D
#individual artist naming
#.pon files have symbols like {ALICORN} and so on.


def load_cards_file(path, save_tsssf_converted=True):
    path = os.path.abspath(path)
    card_set = os.path.split(os.path.dirname(path))[1]
    game_folder = os.path.dirname(os.path.dirname(path))
    game = os.path.split(game_folder)[1]

    with open(path, 'rb') as fp:
        if path.endswith('.json'):
            # new json format
            data = json.loads(fp.read().decode('utf-8-sig', 'replace'))
            module = __import__(data['module'])
        else:
            # old pon format
            first_line = fp.readline().decode('utf-8-sig', 'replace').strip()
            module = __import__(first_line)
            data = {'module': first_line, 'cards': []}

            # convert to new format
            convert_line = getattr(module, 'convert_line', None)
            for line in fp:
                line = line.decode('utf-8', 'replace').strip()
                if not line or line[0] in ('#', ';', '/'):
                    continue
                line = line.replace(r'\r', '')
                if convert_line:
                    line = convert_line(line)
                data['cards'].append(line)

    data['game'] = game
    data['card_set'] = card_set

    # prepare cards
    data['cards'] = unpack_card_group(data['cards'], data.get('default'))
    data['cards'] = select_focused_cards(data['cards'])

    if not path.endswith('.json') and save_tsssf_converted and data['module'] == 'TSSSF_CardGen':
        print 'Converting to new format!'
        jsonpath = os.path.splitext(path)[0] + '.json'
        if os.path.exists(jsonpath):
            raise Exception("json file exists, cannot convert")
        with open(jsonpath, 'wb') as fp:
            fp.write(fancy_json_cards(data).encode('utf-8'))

    return module, data


def unpack_card_group(cards, group=None):
    union_dicts = ('fonts', 'colors', 'anchors', 'anchors_offset', 'leading')
    if not group:
        group = {}
    unpacked_cards = []
    for card in cards:
        if 'group' in card and 'cards' in card:
            new_group = dict(group)
            for key, value in card['group'].items():
                if key not in union_dicts or key not in new_group:
                    new_group[key] = value
                    continue
                new_group[key] = new_group[key].copy()
                new_group[key].update(value)

            unpacked_cards.extend(unpack_card_group(card['cards'], new_group))
        else:
            new_card = dict(group)
            for key, value in card.items():
                if key not in union_dicts or key not in new_card:
                    new_card[key] = value
                    continue
                new_card[key] = new_card[key].copy()
                new_card[key].update(value)
            unpacked_cards.append(new_card)
    return unpacked_cards


def select_focused_cards(cards):
    focused = []
    for card in cards:
        if card.get('focus') and not card.get('disable'):
            focused.append(card)
    if not focused:
        for card in cards:
            if not card.get('disable'):
                focused.append(card)
    return focused


def fancy_json_cards(data):
    from collections import OrderedDict

    taglist = ('type', 'picture', 'symbols', 'title', 'keywords', 'body', 'flavor', 'expansion', 'client')
    cards = []
    for tags in data['cards']:
        dtags = []
        for tag in taglist:
            if tag in tags:
                dtags.append((tag, tags[tag]))
        cards.append(OrderedDict(dtags))

    odata = [('module', data['module']), ('cards', cards)]
    odata = OrderedDict(odata)
    return json.dumps(odata, sort_keys=False, indent=1, ensure_ascii=False)

def load_translation_files(folder, card_set, module):
    # Custom translations: using translation.json file from card set folder and from game folder
    count = 0
    for tpath in (os.path.join(folder, 'translation.json'), os.path.join(folder, card_set, 'translation.json')):
        if not os.path.isfile(tpath):
            continue

        with open(tpath, 'rb') as fp:
            translation = json.loads(fp.read().decode('utf-8-sig', 'replace'))

        count += 1

        if 'RulesDict' in translation:
            module.RulesDict.update(translation['RulesDict'])
        if 'CopyrightString' in translation:
            module.CopyrightString = translation['CopyrightString']
        if 'ArtArtist' in translation:
            module.ARTIST = translation['ArtArtist']

    return count


def build_cards(module, data):
    module.CardSet = data['card_set']
    card_set_path = os.path.join(data['game'], data['card_set'])

    if 'resources' in data and getattr(module, 'LoadResources', None):
        module.LoadResources(data['resources'])


    # Create workspace for card images
    workspace_path = CleanDirectory(path=card_set_path, mkdir="workspace", rmstring="*.*")
    module.workspace_path = workspace_path

    # Create image directories
    bleed_path = CleanDirectory(path=card_set_path, mkdir="bleed-images", rmstring="*.*")
    module.BleedsPath = bleed_path
    cropped_path = CleanDirectory(path=card_set_path, mkdir="cropped-images", rmstring="*.*")
    module.CropPath = cropped_path
    vassal_path = CleanDirectory(path=card_set_path, mkdir="vassal-images", rmstring="*.*")
    module.VassalPath = vassal_path

    # Create output directory
    output_folder = CleanDirectory(path=data['game'], mkdir=data['card_set'], rmstring="*.pdf")
    module.CardSetPath = output_folder

    pdf = data.get('pdf', {})

    page_params = {'extension': pdf.get('pages_extension', 'png')}
    if 'dpi' in pdf:
        page_params['dpi'] = pdf['dpi']
    if 'cut_line_width' in pdf:
        page_params['cut_line_width'] = pdf['cut_line_width']
    if 'page' in pdf:
        page_params['page_width'] = pdf['page'][0]
        page_params['page_height'] = pdf['page'][1]
    if 'grid' in pdf:
        page_params['grid_width'] = pdf['grid'][0]
        page_params['grid_height'] = pdf['grid'][1]
    else:
        page_params['grid_width'] = module.PAGE_WIDTH
        page_params['grid_height'] = module.PAGE_HEIGHT

    cards_per_page = page_params['grid_width'] * page_params['grid_height']

    # Make pages
    card_list = []
    back_list = []
    page_num = 0
    count = len(data['cards'])
    for index, card in enumerate(data['cards'], 1):
        label = card.get('title') or card.get('picture') or card.get('type')
        print '[{}/{}] {}'.format(index, count, label.replace('\n', ' ').encode(sys.stdout.encoding, 'replace'))
        card_list.append(module.BuildCard(card))
        back_list.append(module.BuildBack(card))
        # If the card_list is big enough to make a page
        # do that now, and set the card list to empty again
        if len(card_list) >= cards_per_page:
            page_num += 1
            print "Building Page {}...".format(page_num)
            BuildPage(card_list, page_num, workspace_path, **page_params)
            BuildBack(back_list, page_num, workspace_path, **page_params)
            card_list = []
            back_list = []

    # If there are leftover cards, fill in the remaining
    # card slots with blanks and gen the last page
    if len(card_list) > 0:
        # Fill in the missing slots with blanks
        while len(card_list) < cards_per_page:
            card_list.append(module.BuildCard({"type": "BLANK"}))
            back_list.append(module.BuildCard({"type": "BLANK"}))
        page_num += 1
        print "Building Page {}...".format(page_num)
        BuildPage(card_list, page_num, workspace_path, **page_params)
        BuildBack(back_list, page_num, workspace_path, **page_params)

    #Build Vassal
    module.CompileVassalModule()

    return workspace_path, output_folder


def generate_pdf(workspace_path, output_folder, card_set):
    if sys.platform == 'win32':
        print "\nCreating PDF (Windows)..."
        if os.path.isfile(r'imagemagick\convert.exe'):
            # on windows it working only with ascii path
            os.system(ur'imagemagick\convert.exe "{}/page_*.*" "{}/{}.pdf"'.format(
                workspace_path.decode('utf-8'),
                output_folder,
                card_set
                ))
            print "\nCreating PDF of backs..."
            os.system(ur'imagemagick\convert.exe "{}/backs_*.*" "{}/backs_{}.pdf"'.format(
                workspace_path.decode('utf-8'),
                output_folder,
                card_set
                ))
            print "Done!"
        else:
            print "Please download and unpack ImageMagick for Windows into imagemagick directory"
            print "PDF was not created"

    else:
        print "\nCreating PDF (*nix)..."
        os.system(ur'convert "{}/page_*.*" "{}/{}.pdf"'.format(
            workspace_path.decode('utf-8'),
            output_folder,
            card_set
            ).encode('utf-8'))
        print "\nCreating PDF of backs..."
        os.system(ur'convert "{}/backs_*.*" "{}/backs_{}.pdf"'.format(
            workspace_path.decode('utf-8'),
            output_folder,
            card_set
            ).encode('utf-8'))
        print "Done!"


def main(folder=".", filepath="deck.cards"):
    if isinstance(folder, str):
        folder = folder.decode('utf-8', 'replace')
    if isinstance(filepath, str):
        filepath = filepath.decode('utf-8', 'replace')

    module, data = load_cards_file(os.path.join(folder, filepath))
    load_translation_files(data['game'], data['card_set'], module)
    workspace_path, output_folder = build_cards(module, data)
    generate_pdf(workspace_path, output_folder, data['card_set'])

if __name__ == '__main__':
    #main('TSSSF', '1.1.0 Patch/cards.pon')
    #main('TSSSF', '2014 Con Exclusives/cards.pon')
    #main('TSSSF', 'BABScon 2015/cards.pon')
    #main('TSSSF', 'Core 1.0.5/cards.pon')
    #main('TSSSF', 'Core 1.0.5 Delta/cards.pon')
    #main('TSSSF', 'Core 1.1.0/cards.pon')
    #main('TSSSF', 'Core 1.1.0 Test/cards.pon')
    #main('TSSSF', 'Custom Card for/cards.pon')
    #main('TSSSF', 'Extra Credit 0.10.4/cards.pon')
    main('TSSSF', 'Indiegogo/cards.json')
    #main('TSSSF', 'Patreon Expansion 1/cards.pon')
    #main('TSSSF', 'Ponycon Panel 2015/cards.pon')
    #main('TSSSF', 'Ponyville University 0.0.2/cards.pon')
    #main('TSSSF', 'Ponyville University 1.0.1/cards.pon')
    #main('TSSSF', 'Ponyville University 1.0.2/cards.pon')
    #main('TSSSF', 'Thank You/cards.pon')
    #main('BaBOC', 'BaBOC 0.1.0/deck.cards')
