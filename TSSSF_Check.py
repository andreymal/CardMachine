#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import json


def check_cards(cards, ignore_required=(), warnings=False, paths=None):
    if cards is None:
        error("'cards' is not defined")
        return 1

    if not isinstance(cards, list):
        error("'cards' is not list")
        return 1

    if not cards and warnings:
        warning("'cards' is empty")
        return 0

    errors = 0
    for index, card in enumerate(cards, 1):
        errors += check_card(card, ignore_required=ignore_required, warnings=warnings, index=index, paths=paths)

    return errors


def check_card(card, check_required=True, ignore_required=(), warnings=False, paths=None, index='N/A'):
    if 'group' in card or 'cards' in card:
        errors = 0
        if not 'group' in card:
            error("Card group %d: 'group' is not defined" % index)
            errors += 1
        elif not isinstance(card['group'], dict):
            error("Card group %d: 'group' is not dict" % index)
            errors += 1
        else:
            errors += check_card(card['group'], check_required=False, warnings=warnings, paths=paths, index='%s/group' % index)

        if not 'cards' in card:
            error("Card group %d: 'cards' is not defined" % index)
            errors += 1
        elif not isinstance(card['cards'], list):
            error("Card group %d: 'cards' is not list" % index)
            errors += 1
        else:
            for i, c in enumerate(card['cards'], 1):
                new_card = card['group'].copy() if isinstance(card.get('group'), dict) else {}
                new_card.update(c)
                errors += check_card(new_card, ignore_required=ignore_required, warnings=warnings, paths=paths, index='%s/%s' % (index, i))

        return errors

    fancy_index = unicode(card.get('title') or card.get('picture') or card.get('name') or '').replace('\r', '').replace('\n', '')
    if fancy_index:
        index = "%s (%s)" % (index, fancy_index)

    if not isinstance(card, dict):
        error('Card %s: is not dict' % index)
        return 1
    errors = 0
    typ = card.get('type')
    if check_required:
        if typ in ('START', 'Pony', 'Ship', 'Goal'):
            # check required params
            for param in ('picture', 'title', 'keywords', 'body', 'flavor', 'symbols'):
                if typ == 'Goal' and param == 'keywords':
                    continue
                if card.get(param) is None and not param in ignore_required:
                    error('Card %s: required parameter %r is not defined' % (index, param))
                    errors += 1
        elif typ in ('Card', 'Rules1', 'Rules3', 'Rules5'):
            param = 'picture'
            if card.get(param) is None:
                error('Card %s: required parameter %r is not defined' % (index, param))
                errors += 1
        elif typ not in ('BLANK',) and 'type' not in ignore_required:
            error('Card %s: undefined type: %r' % (index, typ))
            errors += 1

    else:
        if 'type' in card and typ not in ('START', 'Pony', 'Ship', 'Goal', 'Card', 'Rules1', 'Rules3', 'Rules5', 'BLANK'):
            error('Card %s: undefined type: %r' % (index, typ))
            errors += 1

    if typ == 'Goal' and 'keywords' in card:
        error("Card %s: 'keywords' is defined for Goal card" % index)
        errors += 1

    # check params type
    for param in ('picture', 'title', 'keywords', 'body', 'flavor', 'overlay', 'expansion', 'client', 'artist', 'timeline_symbol'):
        if param in card and not isinstance(card[param], unicode):
            error('Card %s: parameter %r is not string' % (index, param))
            errors += 1
        elif param in card and not card[param] and warnings and (typ not in ('Ship', 'Goal') or param not in ('keywords', 'body', 'flavor')):
            warning('Card %s: parameter %r is empty' % (index, param))

    # check files
    if warnings and paths:
            if typ == 'Card':
                picture = card.get('picture')
                if picture != "Derpy" and isinstance(picture, unicode) and not os.path.isfile(os.path.join(paths['card_art'], picture + '.png')):
                    warning("Card %s: image 'picture' not found (%s.png)" % (index, picture))
            elif typ == 'Rules1':
                pass
            elif typ == 'Rules3':
                pass
            elif typ == 'Rules5':
                pass
            else:
                for t in ('picture', 'overlay'):
                    if card.get(t) and isinstance(card[t], unicode) and not os.path.isfile(os.path.join(paths['card_art'], card[t])):
                        warning("Card %s: image %r not found (%s)" % (index, t, card[t]))

    # check symbols
    if 'symbols' in card and not isinstance(card['symbols'], list):
        error('Card %s: symbols is not list' % index)
        errors += 1
    elif 'symbols' in card:
        if not card['symbols'] and warnings:
            warning('Card %s: no symbols' % index)
        if len(card['symbols']) > 2:
            error('Card %s: too many symbols (%d), maximum 2' % (index, len(card['symbols'])))
            errors += 1

    if 'timeline_symbol' in card:
        if not isinstance(card['timeline_symbol'], unicode):
            error('Card %s: timeline_symbol is not string' % index)
            errors += 1
        elif warnings and not card['timeline_symbol']:
            warning('Card %s: timeline_symbol is empty' % index)

    # check custom images
    for param in ('frame', 'back'):
        if not param in card:
            continue
        value = card.get(param)
        if not isinstance(value, unicode) or not value or '.' in value:  # do not check identifier
            errors += check_path(value, param, "Card %s" % index, is_font=False, warnings=warnings, paths=paths)

    # check fonts
    if 'fonts' in card:
        fonts = card['fonts']
        if not isinstance(fonts, dict):
            error("Card %s: 'fonts' is not dict" % index)
            errors += 1

        else:
            font_types = ('Title', 'TitleSmall', 'Body', 'BodySmall', 'BodyChangeling', 'Bar', 'BarSmall', 'Flavortext', 'Copyright')
            for font, value in fonts.items():
                if not isinstance(font, unicode):
                    error("Card %s: font key %r is not string" % (index, font))
                    errors += 1
                elif not font:
                    error("Card %s: empty font key" % index)
                    errors += 1
                elif warnings and font not in font_types:
                    warning("Card %s: unknown font key %r" % (index, font))
                errors += check_path(value, param, "Card %s" % index, is_font=True, warnings=warnings, paths=paths)

    # check colors
    if 'colors' in card:
        colors = card['colors']
        if not isinstance(colors, dict):
            error("Card %s: 'colors' is not dict" % index)
            errors += 1

        else:
            color_types = ('main', 'bar text', 'flavor', 'Copyright')
            for color, value in colors.items():
                if not isinstance(color, unicode):
                    error("Card %s: color key %r is not string" % (index, color))
                    errors += 1
                elif not color:
                    error("Card %s: empty color key" % index)
                    errors += 1
                elif warnings and color not in color_types:
                    warning("Card %s: unknown color key %r" % (index, color))

                if not isinstance(value, list):
                    error("Card %s: color value %r is not list" % (index, color))
                    errors += 1
                elif len(value) != 3:
                    error("Card %s: color value %r length is not 3" % (index, color))
                    errors += 1

                for i, c in enumerate(value, 1):
                    if not isinstance(c, int):
                        error("Card %s: color index %r/%d is not int" % (index, color, i))
                        errors += 1
                    elif c < 0:
                        error("Card %s: color index %r/%d is negative" % (index, color, i))
                        errors += 1
                    elif c > 255:
                        error("Card %s: color index %r/%d is greater 255" % (index, color, i))
                        errors += 1

    # check anchors
    for a in ('anchors', 'anchors_offset'):
        if a in card:
            anchors = card[a]
            if not isinstance(anchors, dict):
                error("Card %s: %r is not dict" % (index, a))
                errors += 1

            else:
                anchor_types = (
                     'PonyArt', 'ShipArt', 'GoalArt', 'Symbol1', 'Symbol2', 'TimelineSymbol',
                     'LoneSymbol', 'GoalSymbol2', 'Title', 'TitleTwoLine', 'TitleSmall',
                     'Bar', 'Body', 'BodyShiftedUp', 'Flavor', 'Expansion', 'Copyright'
                )
                for anchor, value in anchors.items():
                    if not isinstance(anchor, unicode):
                        error("Card %s: anchor key %r is not string" % (index, anchor))
                        errors += 1
                    elif not anchor:
                        error("Card %s: empty anchor key" % index)
                        errors += 1
                    elif warnings and anchor not in anchor_types:
                        warning("Card %s: unknown anchor key %r" % (index, anchor))

                    if not isinstance(value, list):
                        error("Card %s: anchor value %r is not list" % (index, anchor))
                        errors += 1
                    elif len(value) != 2:
                        error("Card %s: anchor value %r length is not 2" % (index, anchor))
                        errors += 1

                    for i, c in enumerate(value, 1):
                        if not isinstance(c, int):
                            error("Card %s: anchor index %r/%d is not int" % (index, anchor, i))
                            errors += 1

    # check leading
    if 'leading' in card:
        leading = card['leading']
        if not isinstance(leading, dict):
            error("Card %s: 'leading' is not dict" % index)
            errors += 1

        else:
            leading_types = ('Title', 'TitleTwoLine', 'Body', 'BodyChangeling', 'Flavor')
            for key, value in leading.items():
                if not isinstance(key, unicode):
                    error("Card %s: leading key %r is not string" % (index, key))
                    errors += 1
                elif not key:
                    error("Card %s: empty leading key" % index)
                    errors += 1
                elif warnings and key not in leading_types:
                    warning("Card %s: unknown leading key %r" % (index, key))

                if not isinstance(value, int):
                    error("Card %s: leading value %r is not int" % (index, key))
                    errors += 1

    # check extension
    if 'extension' in card and not isinstance(card['extension'], unicode):
        error("Card %s: 'extension' is not string" % index)
        errors += 1
    elif 'extension' in card and not card['extension']:
        error("Card %s: 'extension' is empty" % index)
        errors += 1

    return errors


def check_path(value, param, identifier, is_font=False, warnings=False, paths=None):
    if isinstance(value, unicode):
        value = ["resource", value]
    if not value:
        error("%s: path %r is empty" % (identifier, param))
        return 1
    if not isinstance(value, list):
        error("%s: path %r is not list" % (identifier, param))
        return 1
    if len(value) < 2:
        error("%s: path %r length is not 2" % (identifier, param))
        return 1
    
    errors = 0
    path_types = ('card_art', 'resource', 'local')
    if value[0] not in path_types:
        error("%s: path %r has unknown type %r" % (identifier, param, value[0]))
        errors += 1

    if is_font and len(value) >= 3:
        if warnings and len(value) > 3:
            warning("%s: path %r has too many items" % (identifier, param))
        if not isinstance(value[2], int):
            error("%s: font size %r is not int: %r" % (identifier, param, value[2]))
            errors += 1
        elif value[2] < 0:
            error("%s: font size %r is negative" % (identifier, param))
            errors += 1
        elif warnings and value[2] < 2:
            warning("%s: font size %r is too small" % (identifier, param))

    if not isinstance(value[1], unicode):
        error("%s: path %r value is not string" % (identifier, param))
        errors += 1
    elif not value[1] and warnings:
        warning("%s: path %r value is empty" % (identifier, param))
    elif warnings and value[0] in path_types and not os.path.isfile(os.path.join(paths[value[0]], value[1])):
        warning("%s: file %r not found (%s)" % (identifier, param, value[1]))

    return errors


def check_defaults(default, warnings=False, paths=None):
    return check_card(default, check_required=False, warnings=warnings, paths=paths, index='"default"')


def check_resources(resources, warnings=False, paths=None):
    errors = 0
    for who in ('symbols', 'frames', 'backs'):
        if who in resources:
            if not isinstance(resources[who], dict):
                error("%r is not dict" % who)
                errors += 1

            else:
                for key, value in resources[who].items():
                    if not isinstance(key, unicode):
                        error("%s name %r is not string" % (who, key))
                        errors += 1
                    elif not key:
                        error("Empty %s" % who)
                        errors += 1

                    if warnings and paths:
                        errors += check_path(value, key, who, is_font=False, warnings=warnings, paths=paths)

    return errors


def check_pdf(pdf, warnings=False, paths=None):
    if pdf is None:
        return 0
    
    if not isinstance(pdf, dict):
        error("'pdf' is not dict")
        return 1

    errors = 0

    # check extension
    if 'pages_extension' in pdf and not isinstance(pdf['pages_extension'], unicode):
        error("pdf 'pages_extension' is not string")
        errors += 1
    elif 'pages_extension' in pdf and not pdf['pages_extension']:
        error("pdf 'pages_extension' is empty")
        errors += 1

    if 'page' in pdf:
        page = pdf['page']
        if not isinstance(page, list):
            error("pdf 'page' is not dict")
            errors += 1
        elif len(page) != 2:
            error("pdf 'page' length is not 2")
            errors += 1

        for index, value in enumerate(page, 1):
            if not isinstance(value, (int, float, long)):
                error("pdf 'page'/%d is not number: %r" % (index, value))
                errors += 1
            elif value <= 0:
                error("pdf 'page'/%d is too small: %r" % (index, value))

    if 'grid' in pdf:
        grid = pdf['grid']
        if not isinstance(grid, list):
            error("pdf 'grid' is not dict")
            errors += 1
        elif len(grid) != 2:
            error("pdf 'grid' length is not 2")
            errors += 1

        for index, value in enumerate(grid, 1):
            if not isinstance(value, (int)):
                error("pdf 'grid'/%d is not int: %r" % (index, value))
                errors += 1
            elif value <= 0:
                error("pdf 'grid'/%d is too small: %r" % (index, value))
                errors += 1

    if 'cut_line_width' in pdf and not isinstance(pdf['cut_line_width'], int):
        error("pdf 'cut_line_width' is not int")
        errors += 1
    elif 'cut_line_width' in pdf and pdf['cut_line_width'] < 0:
        error("pdf 'cut_line_width' is negative")
        errors += 1

    return errors


def warning(*args):
    print "Warning"
    print "",
    for x in args:
        print x,
    print
    print


def error(*args):
    print "Error"
    print "",
    for x in args:
        print x,
    print
    print


def check_file(path, data, warnings=False):
    paths = {
        "resource": os.path.join(os.path.dirname(os.path.dirname(path)), "resources"),
        "card_art": os.path.join(os.path.dirname(os.path.dirname(path)), "Card Art"),
        "local": os.path.dirname(path)
    }
    errors = 0
    errors += check_cards(data.get('cards'), ignore_required=data['default'].keys() if isinstance(data.get('default'), dict) else (), warnings=warnings, paths=paths)
    errors += check_defaults(data.get('default'), warnings=warnings, paths=paths)
    if 'resources' in data:
        errors += check_resources(data['resources'], warnings=warnings, paths=paths)
    errors += check_pdf(data.get('pdf'), warnings=warnings, paths=paths)
    return errors


def main(path=None):
    args = sys.argv[1:]
    if '-W' in args:
        warnings = True
        args.remove('-W')
    else:
        warnings = False
    if not path and not args:
        print("Usage: %s [-W] cards.json" % sys.argv[0])
        return 2

    if args:
        path = args[-1]

    try:
        data = json.loads(open(path, "rb").read().decode('utf-8-sig'))
    except Exception as exc:
        error("Cannot load %s: %s" % (path, exc))
        return 3

    if not data.get('module'):
        error("'module' is not defined")
        return 1
    if data['module'] != 'TSSSF_CardGen':
        error("I can check only TSSSF_CardGen")
        return 3

    return 1 if check_file(os.path.abspath(path), data, warnings=warnings) > 0 else 0


if __name__ == "__main__":
    main("TSSSF/Indiegogo/cards.json")
