import os
import random
import traceback
import PIL_Helper

TYPE, PICTURE, SYMBOLS, TITLE, KEYWORDS, BODY, FLAVOR, EXPANSION, CLIENT = range(9)
DIRECTORY = "TSSSF"
ARTIST = "Pixel Prism"

def convert_line(line):
    old_tags = line.replace(r'\n', '\n').split('`')
    taglist = ('type', 'picture', 'symbols', 'title', 'keywords', 'body', 'flavor', 'expansion', 'client')
    new_tags = {}
    for index, tag in enumerate(taglist):
        if index >= len(old_tags):
            break
        value = old_tags[index]
        if index == 2:  # SYMBOLS
            value = value.split('!')
            if 'Dystopian' in value:
                new_tags['timeline_symbol'] = 'Dystopian'
                value.remove('Dystopian')
        new_tags[tag] = value
    return new_tags

LegacySymbolMode = False
PAGE_WIDTH = 3
PAGE_HEIGHT = 3
TOTAL_CARDS = PAGE_WIDTH*PAGE_HEIGHT


workspace_path = os.path.dirname("workspace")
card_set = os.path.dirname("deck.cards")
CardSet = os.path.dirname("deck.cards")
CardPath = DIRECTORY+"/Card Art/"
ResourcePath = DIRECTORY+"/resources/"
BleedsPath = DIRECTORY+"/bleed-images/"
CropPath = DIRECTORY+"/cropped-images/"
VassalPath = DIRECTORY+"/vassal-images/"
CardSetPath = DIRECTORY+"/"

VassalTemplatesPath = DIRECTORY+"/vassal templates/"
VassalWorkspacePath = DIRECTORY+"/vassal workspace/"
VassalImagesPath = os.path.join(VassalWorkspacePath, "images")
VASSAL_SCALE=(260,359)

VassalCard = [0]
ART_WIDTH = 600
base_w = 889
base_h = 1215
base_w_center = base_w/2
base_h_center = base_h/2
w_marg = 31
h_marg = 36
baserect=[(w_marg,h_marg),(base_w-w_marg,base_h-h_marg)]
textmaxwidth = 689

croprect=(50,63,788+50,1088+63)

TextHeightThresholds = [363, 378, 600]
TitleWidthThresholds = [50] #This is in #characters, fix later plox
BarTextThreshold = [500]

fontsizes = {
    "Title": 55,
    "TitleSmall": 45,
    "Body": 35,
    "BodySmall": 35,
    "BodyChangeling": 31,
    "Bar": 38,
    "BarSmall": 35,
    "Flavortext": 28,
    "Copyright": 18
}

fonts = {
    "Title":PIL_Helper.BuildFont(ResourcePath+"TSSSFBartholomew-Bold.otf", fontsizes["Title"]),
    "TitleSmall":PIL_Helper.BuildFont(ResourcePath+"TSSSFBartholomew-Bold.otf", fontsizes["TitleSmall"]),
    "Body":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", fontsizes["Body"]),
    "BodySmall":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", fontsizes["BodySmall"]),
    "BodyChangeling":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", fontsizes["BodyChangeling"]),
    "Bar":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", fontsizes["Bar"]),
    "BarSmall":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", fontsizes["BarSmall"]),
    "Flavortext":PIL_Helper.BuildFont(ResourcePath+"KlinicSlabBookIt.otf", fontsizes["Flavortext"]),
    "Copyright":PIL_Helper.BuildFont(ResourcePath+"TSSSFCabin-Medium.ttf", fontsizes["Copyright"])
}

custom_fonts = {}

Anchors = {
    "Blank": (base_w_center, 300),
    "PonyArt": (173, 225),
    "ShipArt": (173, 226),
    "GoalArt": (174, 224),
    "Symbol1": (58+50,56+63),
    "Symbol2": (58+50,160+63),
    "LoneSymbol": (108,153),
    "TimelineSymbol": (58+50,535+63),
    "GoalSymbol2": (108,613),
    "Title": (-65-50, 160),
    "TitleTwoLine": (-65-50, 159),
    "TitleSmall": (-65-50, 157),
    "Bar": (-68-50, 598+67),
    "Body": (base_w_center, 735),
    "BodyShiftedUp": (base_w_center, 730),
    "Flavor": (base_w_center, -110),
    "Expansion": (640+50, 525+63),
    "Copyright": (-38-50, -13-61)
}

ArtMissing = [
    PIL_Helper.LoadImage(CardPath+"/artmissing01.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing02.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing03.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing04.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing05.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing06.png"),
    PIL_Helper.LoadImage(CardPath+"/artmissing07.png"),
    ]

Frames = {
    "START": PIL_Helper.LoadImage(ResourcePath+"/BLEED-Blank-Start.png"),
    "Warning": PIL_Helper.LoadImage(CardPath+"/BLEED_Card - Warning.png"),
    "Pony": PIL_Helper.LoadImage(ResourcePath+"/BLEED-Blank-Pony.png"),
    "Ship": PIL_Helper.LoadImage(ResourcePath+"/BLEED-Blank-Ship.png"),
    "Rules1": PIL_Helper.LoadImage(CardPath+"/BLEED_Rules1.png"),
    "Rules3": PIL_Helper.LoadImage(CardPath+"/BLEED_Rules3.png"),
    "Rules5": PIL_Helper.LoadImage(CardPath+"/BLEED_Rules5.png"),
    "Goal": PIL_Helper.LoadImage(ResourcePath+"/BLEED-Blank-Goal.png"),
    "Derpy": PIL_Helper.LoadImage(CardPath+"/BLEED_Card - Derpy Hooves.png"),
    "TestSubject": PIL_Helper.LoadImage(CardPath+"/BLEED_Card - OverlayTest Subject Cheerilee.png")
    }

CustomFrames = {}

Symbols = {
    "male": PIL_Helper.LoadImage(ResourcePath+"/Symbol-male.png"),
    "female": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Female.png"),
    "malefemale": PIL_Helper.LoadImage(ResourcePath+"/Symbol-MaleFemale.png"),
    "earth pony": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Earth-Pony.png"),
    "unicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Unicorn.png"),
    "uniearth": PIL_Helper.LoadImage(ResourcePath+"/symbol-uniearth.png"),
    "pegasus": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Pegasus.png"),
    "alicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Alicorn.png"),
    "changelingearthpony": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingEarthPony.png"),
    "changelingunicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingUnicorn.png"),
    "changelingpegasus": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingPegasus.png"),
    "changelingalicorn": PIL_Helper.LoadImage(ResourcePath+"/Symbol-ChangelingAlicorn.png"),
    "dystopian": PIL_Helper.LoadImage(ResourcePath+"/symbol-dystopian-future.png"),
    "ship": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Ship.png"),
    "goal": PIL_Helper.LoadImage(ResourcePath+"/Symbol-Goal.png"),
    "0": PIL_Helper.LoadImage(ResourcePath+"/symbol-0.png"),
    "1": PIL_Helper.LoadImage(ResourcePath+"/symbol-1.png"),
    "2": PIL_Helper.LoadImage(ResourcePath+"/symbol-2.png"),
    "3": PIL_Helper.LoadImage(ResourcePath+"/symbol-3.png"),
    "4": PIL_Helper.LoadImage(ResourcePath+"/symbol-4.png"),
    "3-4": PIL_Helper.LoadImage(ResourcePath+"/symbol-34.png"),
    "2-3": PIL_Helper.LoadImage(ResourcePath+"/symbol-23.png")
    }

Expansions = {
    "Everfree14": PIL_Helper.LoadImage(ResourcePath+"/symbol-Everfree14.png"),
    "Indiegogo": PIL_Helper.LoadImage(ResourcePath+"/symbol-Indiegogo.png"),
    "Birthday": PIL_Helper.LoadImage(ResourcePath+"/symbol-birthday.png"),
    "Bronycon": PIL_Helper.LoadImage(ResourcePath+"/symbol-Bronycon14.png"),
    "Summer": PIL_Helper.LoadImage(ResourcePath+"/symbol-summer-lovin.png"),
    "Apricity": PIL_Helper.LoadImage(ResourcePath+"/symbol-apricity.png"),
    "BronyCAN": PIL_Helper.LoadImage(ResourcePath+"/symbol-Bronycan14.png"),
    "Xtra": PIL_Helper.LoadImage(ResourcePath+"/symbol-extracredit.png"),
    "Xtra-dark": PIL_Helper.LoadImage(ResourcePath+"/symbol-extracredit-black.png"),
    "NMND": PIL_Helper.LoadImage(ResourcePath+"/symbol-nightmarenights.png"),
    "Ciderfest": PIL_Helper.LoadImage(ResourcePath+"/symbol-ponyvilleciderfest.png"),
    "Adventure": PIL_Helper.LoadImage(ResourcePath+"/symbol-adventure.png"),
    "Custom": PIL_Helper.LoadImage(ResourcePath+"/symbol-custom.png"),
    "Power": PIL_Helper.LoadImage(ResourcePath+"/symbol-power.png"),
    "Multiplicity": PIL_Helper.LoadImage(ResourcePath+"/symbol-multiplicity.png"),
    "Canon": PIL_Helper.LoadImage(ResourcePath+"/symbol-canon.png"),
    "Dungeon": PIL_Helper.LoadImage(ResourcePath+"/symbol-dungeon.png"),
    "50": PIL_Helper.LoadImage(ResourcePath+"/symbol-50.png"),
    "2014": PIL_Helper.LoadImage(ResourcePath+"/symbol-2014.png"),
    "Hearthswarming": PIL_Helper.LoadImage(ResourcePath+"/symbol-hearthswarming.png"),
    "Ponycon 2015": PIL_Helper.LoadImage(ResourcePath+"/symbol-ponynyc.png"),
    "Patreon": PIL_Helper.LoadImage(ResourcePath+"/symbol-Patreon.png"),
    "Gameshow": PIL_Helper.LoadImage(ResourcePath+"/symbol-gameshow.png"),
    "BABScon": PIL_Helper.LoadImage(ResourcePath+"/symbol-BABScon.png")
    }

ColorDict={
    "START": (58, 50, 53),
    "START bar text": (237, 239, 239),
    "START flavor": (28, 20, 23),
    "Pony": (70, 44, 137),
    "Pony bar text": (234, 220, 236),
    "Pony flavor": (25, 2, 51),
    "Goal": (18, 57, 98),
    "Goal flavor": (7, 34, 62),
    "Shipwrecker": (8, 57, 98),
    "Shipwrecker flavor": (0, 34, 62),
    "Ship": (206, 27, 105),
    "Ship bar text": (234, 220, 236),
    "Ship flavor": (137, 22, 47),
    "Copyright": (255, 255, 255),
    "Blankfill": (200,200,200)
    }

RulesDict={
    "{replace}": "While in your hand, you may discard a Pony card from the grid and play this card in its place. This power cannot be copied.",
    "{swap}": "You may swap 2 Pony cards on the shipping grid.",
    "{3swap}": "You may swap up to 3 Pony cards on the grid.",
    "{draw}": "You may draw a card from the Ship or Pony deck.",
    "{goal}": "You may discard a Goal and draw a new one to replace it.",
    "{search}": "You may search the Ship or Pony discard pile for a card of your choice and play it.",
    "{copy}": "You may copy the power of any Pony card currently on the shipping grid, except for Changelings.",
    "{hermaphrodite}": "May count as either {male} or {female} for all Goals, Ships, and powers.",
    "{double pony}": "This card counts as 2 Ponies.",
    "{love poison}": "Instead of playing this ship with a Pony card from your hand, or connecting two ponies already on the grid, take a Pony card from the shipping grid and reattach it elsewhere with this Ship. That card's power activates.",
    "{keyword change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card counts as having any one keyword of your choice, except pony names.",
    "{gender change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card becomes the opposite gender.",
    "{race change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card becomes a race of your choice. This cannot affect Changelings.",
    "{timeline change}": "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card counts as {postapocalypse}.",
    "{play from discard}": "You may choose to play the top card on the Pony discard pile with this Ship, rather than use a Pony card from your hand.",
    }

backs = {"START": PIL_Helper.LoadImage(ResourcePath + "Back-Start.png"),
         "Pony": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
         "Goal": PIL_Helper.LoadImage(ResourcePath + "Back-Goals.png"),
         "Ship": PIL_Helper.LoadImage(ResourcePath + "Back-Ships.png"),
         "Card": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
         "Shipwrecker": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
         "BLANK": PIL_Helper.LoadImage(ResourcePath + "Blank - Intentionally Left Blank.png"),
         "Rules1": PIL_Helper.LoadImage(CardPath + "Rules2.png"),
         "Rules3": PIL_Helper.LoadImage(CardPath + "Rules4.png"),
         "Rules5": PIL_Helper.LoadImage(CardPath + "Rules6.png"),
         "TestSubject": PIL_Helper.LoadImage(ResourcePath + "Back-Main.png"),
         "Warning": PIL_Helper.LoadImage(CardPath + "Card - Contact.png")
        }

custom_backs = {}

CopyrightString = u"{}; TSSSF by Horrible People Games. Art by {}."

def ParseCustomPath(custom_item):
    """
    "foo.png" => "TSSSF/resources/foo.png"
    ["resource", "foo.png"] => "TSSSF/resources/foo.png"
    ["card_art", "foo.png"] => "TSSSF/Card Art/foo.png"
    ["local", "foo.png"] => "TSSSF/card_set_folder/foo.png"
    """
    if isinstance(custom_item, basestring):
        return os.path.join(ResourcePath, custom_item)
    if custom_item[0] == "card_art":
        path = os.path.join(CardPath, custom_item[1])
    elif custom_item[0] == "resource":
        path = os.path.join(ResourcePath, custom_item[1])
    elif custom_item[0] == "local":
        path = os.path.join(CardSetPath, custom_item[1])
    else:
        raise ValueError("Unknown path type: %r" % custom_item[0])
    return path

def GetCustomImage(custom_cache, custom_item):
    if isinstance(custom_item, unicode):
        custom_item = ('resource', custom_item)
    else:
        custom_item = tuple(custom_item[:2])
    if custom_item not in custom_cache:
        path = ParseCustomPath(custom_item)
        custom_cache[custom_item] = PIL_Helper.LoadImage(path)
    return custom_cache[custom_item]

def GetFont(typ, tags=None):
    if not tags or 'fonts' not in tags or typ not in tags['fonts']:
        return fonts[typ]
    custom_item = tags['fonts'][typ]
    if isinstance(custom_item, unicode):
        custom_item = ('resource', custom_item)
    else:
        custom_item = tuple(custom_item[:3])
    if len(custom_item) < 3:
        custom_item = (custom_item[0], custom_item[1], fontsizes[typ])
    if not custom_item in custom_fonts:
        path = ParseCustomPath(custom_item)
        custom_fonts[custom_item] = PIL_Helper.BuildFont(path, custom_item[2])
    return custom_fonts[custom_item]

def GetLeading(typ, tags=None, default=0):
    if not tags or not 'leading' in tags:
        return default
    return tags['leading'].get(typ, default)

def GetAnchor(typ, tags=None):
    if not tags or 'anchors' not in tags:
        anchor = Anchors[typ]
    else:
        anchor = tags['anchors'].get(typ) or Anchors[typ]
    if tags and 'anchors_offset' in tags:
        anchor_offset = tags['anchors_offset'].get(typ, (0, 0))
        anchor = tuple(sum(x) for x in zip(anchor, anchor_offset))
    return anchor

def GetColor(tags, param=""):
    if 'colors' in tags and (param or "main") in tags['colors']:
        return tuple(tags['colors'][param or "main"])
    key = "{} {}".format(tags['type'], param) if param else tags['type']
    return ColorDict.get(key) or ColorDict[param]

def LoadResources(data):
    if 'symbols' in data:
        for sym, path in data['symbols'].items():
            Symbols[sym.lower()] = PIL_Helper.LoadImage(ParseCustomPath(path))

    if 'frames' in data:
        for frame, path in data['frames'].items():
            Frames[frame] = PIL_Helper.LoadImage(ParseCustomPath(path))

    if 'backs' in data:
        for back, path in data['backs'].items():
            backs[back] = PIL_Helper.LoadImage(ParseCustomPath(path))

def FixFileName(tagin, extension):
    FileName = tagin.replace("\n", "")
    invalid_chars = [",", "?", '"', ":"]
    for c in invalid_chars:
        FileName = FileName.replace(c,"")
    FileName = u"{0}.{1}".format(FileName, extension)
    #print FileName
    return FileName

def FixUnicode(text):
    if LegacySymbolMode:
        text=text.replace(';', u"\u2642")
        text=text.replace('*', u"\u2640")
        text=text.replace('>', u"\u26A4")
        #text=text.replace('#', u"\u2714")
        text=text.replace('<', u"\u2764")
        text=text.replace('%', u"\uE000")
        text=text.replace('8', u"\uE001")
        text=text.replace('9', u"\uE002")
        text=text.replace('@', u"\uE003")
        text=text.replace('$', u"\uE004")
    else:
        text=text.replace('{male}', u"\u2642")
        text=text.replace('{female}', u"\u2640")
        text=text.replace('{malefemale}', u"\u26A4")
        #text=text.replace('{goal}', u"\u2714")
        text=text.replace('{ship}', u"\u2764")
        text=text.replace('{earthpony}', u"\uE000")
        text=text.replace('{unicorn}', u"\uE001")
        text=text.replace('{pegasus}', u"\uE002")
        text=text.replace('{alicorn}', u"\uE003")
        text=text.replace('{postapocalypse}', u"\uE004")
    return text

def SaveCard(filepath, image_to_save):
    '''
    If the filepath already exists, insert _001 just before the
    extension. If that exists, increment the number until we get to
    a filepath that doesn't exist yet.
    '''
    if image_to_save.mode != "RGB":
        image_to_save = image_to_save.convert("RGB")
    if os.path.exists(filepath):
        basepath, extension = os.path.splitext(filepath)
        i = 0
        while os.path.exists(filepath):
            i += 1
            filepath = u"{}_{:>03}{}".format(basepath, i, extension)
    image_to_save.save(filepath, dpi=(300, 300))

def BuildCard(tags):
    try:
        im = PickCardFunc(tags)
        im_crop=im.crop(croprect)
        if tags['type'] not in ('BLANK',) and tags.get('save', True):
            filename = FixFileName(tags['type'] + "_" + (tags.get('title') or tags.get('picture')), tags.get('extension', 'png'))
            SaveCard(os.path.join(BleedsPath, filename), im)
            SaveCard(os.path.join(CropPath, filename), im_crop)

            im_vassal=PIL_Helper.ResizeImage(im_crop, VASSAL_SCALE)
            SaveCard(os.path.join(VassalPath, filename), im_vassal)
        #MakeVassalCard(im_cropped)
    except Exception as e:
        print("Warning, Bad Card: {0}".format(tags))
        traceback.print_exc()
        im_crop = MakeBlankCard().crop(croprect)
    #im.show()  # TEST
    return im_crop

def BuildBack(tags):
    #print("Back type: " + tags['type'])
    if tags.get('back'):
        if tags['back'] in backs:
            return backs[tags['back']]
        return GetCustomImage(custom_backs, tags['back'])
    return backs.get(tags['type'], backs['BLANK'])

def PickCardFunc(tags):
    if tags['type'] == "START":
        return MakeStartCard(tags)
    elif tags['type'] == "Pony":
        return MakePonyCard(tags)
    elif tags['type'] == "Ship":
        return MakeShipCard(tags)
    elif tags['type'] == "Goal":
        return MakeGoalCard(tags)
    elif tags['type'] == "BLANK":
        return MakeBlankCard()
    elif tags['type'] in ("Warning", "Rules1", "Rules3", "Rules5"):
        return MakeSpecialCard(tags['type'], custom_frame=tags.get('frame'))
    elif tags['type'] == "TestSubject":
        return MakePonyCard(tags)
    elif tags['type'] == "Card":
        return MakeSpecialCard(tags['picture'], custom_frame=tags.get('frame'))
    else:
        raise Exception("No card of type {0}".format(tags['type']))

def GetFrame(card_type, custom_frame=None):
    if isinstance(custom_frame, unicode) and custom_frame in Frames:
        return Frames[custom_frame].copy()
    if card_type not in Frames and not custom_frame:
        custom_frame = ("resource", card_type + ".png")
    if custom_frame:
        return GetCustomImage(CustomFrames, custom_frame).copy()
    return Frames[card_type].copy()

def AddCardArt(image, filename, anchor):
    if filename == "NOART":
        return
    if os.path.exists(os.path.join(CardPath, filename)):
        art = PIL_Helper.LoadImage(os.path.join(CardPath, filename))
    else:
        art = random.choice(ArtMissing)
    # Find desired height of image based on width of 600 px
    w, h = art.size
    h = int((float(ART_WIDTH)/w)*h)
    # Resize image to fit in frame
    art = PIL_Helper.ResizeImage(art, (ART_WIDTH,h))
    image.paste(art, anchor)

def AddSymbols(image, tags):
    # Remove any timeline symbols from the symbols list
    symbols = [x.lower() for x in tags.get('symbols', ())]
    if tags['type'] == "Goal":
        if len(symbols) != 2:
            raise Exception("Goal should have two symbols")
        positions = [GetAnchor("LoneSymbol", tags), GetAnchor("GoalSymbol2", tags)]
    else:
        if len(symbols) == 1:
            positions = [GetAnchor("LoneSymbol", tags)]
        elif len(symbols) == 2:
            positions = [GetAnchor("Symbol1", tags), GetAnchor("Symbol2", tags)]
        else:
            raise Exception("Too many symbols")

    for index,s in enumerate(symbols):
        sym = Symbols.get(s, None)
        if sym:
            image.paste(sym, positions[index], sym)

    if tags.get('timeline_symbol'):
        s = tags['timeline_symbol'].lower()
        sym = Symbols.get(s, None)
        if sym:
            image.paste(sym, GetAnchor("TimelineSymbol", tags), sym)

def TitleText(image, text, color, tags=None):
    font = GetFont("Title", tags)
    anchor = GetAnchor("Title", tags)
    leading = GetLeading("Title", tags, -9)
    if text.count('\n') > 0:
        anchor = GetAnchor("TitleTwoLine", tags)
        leading = GetLeading("TitleTwoLine", tags, -15)
    if len(text)>TitleWidthThresholds[0]:
        anchor = GetAnchor("TitleSmall", tags)
        font = GetFont("TitleSmall", tags)
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = anchor,
        valign = "center",
        halign = "right",
        leading_offset = leading
        )

def BarText(image, text, color, tags=None):
    bar_text_size = PIL_Helper.GetTextBlockSize(text,GetFont("Bar", tags),textmaxwidth)
    if bar_text_size[0] > BarTextThreshold[0]:
        font = GetFont("BarSmall", tags)
    else:
        font = GetFont("Bar", tags)
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = GetAnchor("Bar", tags),
        halign = "right"
        )

def BodyText(image, text, color, flavor_text_size=0, font=None, tags=None):
    # Replacement of keywords with symbols
    for keyword in RulesDict:
        if keyword in text:
            text = text.replace(keyword, RulesDict[keyword])
    text = FixUnicode(text)
    if font is None:
        font = GetFont("Body", tags)
    anchor = GetAnchor("Body", tags)
    leading = GetLeading("Body", tags, -1)
    # Get the size of the body text as (w,h)
    body_text_size = PIL_Helper.GetTextBlockSize(
        text, GetFont("Body", tags), textmaxwidth
        )
    # If the height of the body text plus the height of the flavor text
    # doesn't fit in on the card in the normal position, move the body text up
    if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[0]:
        anchor = GetAnchor("BodyShiftedUp", tags)
    # If they still don't fit, makes the body text smaller
    if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[1]:
        font = GetFont("BodySmall", tags)
        body_text_size = PIL_Helper.GetTextBlockSize(
            text, font, textmaxwidth
            )
        # If they still don't fit, make it smaller again. They're probably
        # the changeling cards
        if body_text_size[1] + flavor_text_size[1] > TextHeightThresholds[1]:
            font = GetFont("BodyChangeling", tags)
            leading = GetLeading("BodyChangeling", tags, -3)
    GetAnchor("BodyShiftedUp", tags)
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = font,
        fill = color,
        anchor = anchor,
        halign = "center",
        max_width = textmaxwidth,
        leading_offset=leading
        )

def FlavorText(image, text, color, tags=None):
    return PIL_Helper.AddText(
        image = image,
        text = text,
        font = GetFont("Flavortext", tags),
        fill = color,
        anchor = GetAnchor("Flavor", tags),
        valign = "bottom",
        halign = "center",
        leading_offset=GetLeading("Flavor", tags, 1),
        max_width = textmaxwidth,
        )

def AddExpansion(image, tags):
    #print "Expansion: {}".format(expansion)
    expansion_symbol = Expansions.get(tags['expansion'], None)
    if expansion_symbol:
        image.paste(expansion_symbol, GetAnchor("Expansion", tags), expansion_symbol)

def CopyrightText(tags, image, color):
    text = tags.get('copyright')
    if not text:
        card_set = CardSet.replace('_',' ')
        #print tags[CLIENT], repr(tags)
        if 'client' in tags:
            card_set += u" " + tags['client']
        text = CopyrightString.format(card_set, tags.get('artist', ARTIST))
    PIL_Helper.AddText(
        image = image,
        text = text,
        font = GetFont("Copyright", tags),
        fill = color,
        anchor = GetAnchor("Copyright", tags),
        valign = "bottom",
        halign = "right",
        )

def MakeBlankCard():
    image = PIL_Helper.BlankImage(base_w, base_h)
    
    PIL_Helper.AddText(
        image = image,
        text = "This Card Intentionally Left Blank",
        font = fonts["Title"],
        fill = ColorDict["Blankfill"],
        anchor = Anchors["Blank"],
        max_width = textmaxwidth
        )    
    return image


def MakeStandardCard(tags, image=None):
    if not image:
        image = GetFrame(tags['type'], tags.get('frame'))
        AddCardArt(image, tags['picture'], GetAnchor("PonyArt", tags))
    TitleText(image, tags['title'], GetColor(tags), tags)
    if tags.get('keywords'):
        BarText(image, tags['keywords'], GetColor(tags, "bar text"), tags)
    text_size = FlavorText(image, tags['flavor'], GetColor(tags, "flavor"), tags)
    BodyText(image, tags['body'], GetColor(tags), text_size, tags=tags)
    CopyrightText(tags, image, tags.get("copyright_color", GetColor(tags, "Copyright")))
    if tags.get('expansion'):
        AddExpansion(image, tags)
    AddSymbols(image, tags)
    if tags.get('overlay'):
        overlay_image = PIL_Helper.LoadImage(CardPath + "/" + tags['overlay'])
        image.paste(overlay_image, (0, 0), overlay_image)
    return image

def MakeStartCard(tags):
    return MakeStandardCard(tags)

def MakePonyCard(tags):
    return MakeStandardCard(tags)

def MakeShipCard(tags):
    image = GetFrame(tags['type'], tags.get('frame'))
    AddCardArt(image, tags['picture'], GetAnchor("ShipArt", tags))
    return MakeStandardCard(tags, image)

def MakeGoalCard(tags):
    image = GetFrame(tags['type'], tags.get('frame'))
    AddCardArt(image, tags['picture'], GetAnchor("GoalArt", tags))
    return MakeStandardCard(tags, image)

def MakeSpecialCard(picture, custom_frame=None):
    return GetFrame(picture, custom_frame)

def InitVassalModule():
    pass

def MakeVassalCard(im):
    VassalCard[0]+=1
    #BuildCard(line).save(VassalImagesPath + "/" + str(VassalCard) + ".png")
    im.save(VassalImagesPath + "/" + str(VassalCard[0]) + ".png")
    
def CompileVassalModule():
    pass

if __name__ == "__main__":
    print("Not a main module. Run GameGen.py")
