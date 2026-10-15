"""Deterministic everyday color labels and palette retrieval; no external dependencies."""
import colorsys
from itertools import permutations
from math import dist


ALIASES = {
    'blue': ('blue', '蓝', '蓝色', '蓝色系'),
    'pink': ('pink', '粉', '粉色', '粉红', '粉红色', '玫红', '玫红色'),
    'yellow': ('yellow', '黄', '黄色', '黄色系'),
    'red': ('red', '红', '红色', '红色系'),
    'orange': ('orange', '橙', '橙色', '橘色', '橘黄色'),
    'green': ('green', '绿', '绿色', '绿色系'),
    'cyan': ('cyan', '青', '青色', '青蓝', '青蓝色', '蓝绿色'),
    'purple': ('purple', '紫', '紫色', '紫色系'),
    'brown': ('brown', '棕', '棕色', '褐色', '咖啡色'),
    'white': ('white', '白', '白色', '米白', '米白色', '奶油白'),
    'gray': ('gray', 'grey', '灰', '灰色', '灰色系'),
    'black': ('black', '黑', '黑色'),
    'any': ('any', '任意', '不限'),
}
NAMES = dict(blue='blue', pink='pink', yellow='yellow', red='red', orange='orange',
             green='green', cyan='cyan', purple='purple', brown='brown', white='white',
             gray='gray', black='black')


def color_info(hex_color):
    rgb = tuple(int(hex_color[i:i+2], 16) / 255 for i in (1, 3, 5))
    hue, lightness, _ = colorsys.rgb_to_hls(*rgb)
    _, saturation, _ = colorsys.rgb_to_hsv(*rgb)
    hue *= 360
    if hue < 15 or hue >= 345:
        family = 'pink' if lightness >= .72 else 'red'
    elif hue < 45:
        family = 'brown' if lightness < .45 or (saturation < .5 and lightness < .65) else 'orange'
    elif hue < 65:
        family = 'brown' if lightness < .38 else 'yellow'
    elif hue < 165:
        family = 'green'
    elif hue < 200:
        family = 'cyan'
    elif hue < 245:
        family = 'blue'
    elif hue < 320:
        family = 'purple'
    else:
        family = 'pink' if lightness >= .35 else 'red'

    tags = [family]
    if saturation < .055 or max(rgb)-min(rgb) < .025 or lightness < .08:
        family = 'black' if lightness < .18 else 'white' if lightness > .93 else 'gray'
        tags = [family]
        name = ('light gray' if lightness >= .75 else 'dark gray' if lightness <= .35 else 'gray') if family == 'gray' else NAMES[family]
    elif lightness > .88 and max(rgb) - min(rgb) < .25:
        name = 'cream' if hue < 65 else {'blue':'blue-tinted white', 'cyan':'cyan-tinted white', 'green':'green-tinted white',
                                           'purple':'purple-tinted white', 'pink':'pink-tinted white', 'red':'pink-tinted white'}[family]
        tags.append('white')
    elif saturation < .18 or (lightness < .35 and saturation < .25):
        name = {'blue':'blue-gray', 'cyan':'cyan-gray', 'purple':'purple-gray', 'pink':'pink-gray',
                'yellow':'warm gray', 'orange':'warm gray', 'red':'warm gray'}.get(family, 'gray-green')
        tags.append('gray')
    else:
        prefix = 'light ' if lightness >= .72 or (saturation < .35 and lightness >= .55) else 'dark ' if lightness <= .35 else ''
        name = prefix + ('yellow-green' if family == 'green' and hue < 85 else NAMES[family])
    return {'hex': hex_color, 'name': name, 'tags': tags,
            'lightness': lightness, 'saturation': saturation, 'chroma':max(rgb)-min(rgb)}


def palette_distance(a, b):
    def rgb(color):
        return tuple(int(color[i:i+2], 16)/255 for i in (1, 3, 5))
    return min(sum(dist(rgb(x), rgb(y)) for x, y in zip(a, order))/3
               for order in permutations(b))


def search(data, query, limit=5, lightness=None, saturation=None):
    if not 1 <= limit <= 100:
        raise ValueError('Recommendation count must be 1–100')
    target = next((key for key, words in ALIASES.items() if query.strip().lower() in words), None)
    if target is None:
        raise ValueError('Use a basic color name (such as blue or pink) or any; use flags for lightness and saturation')
    if lightness not in (None, 'light', 'dark') or saturation not in (None, 'muted', 'vivid'):
        raise ValueError('Unsupported lightness or saturation filter')
    families = {f['id']:f['name'] for f in data['families']}
    candidates = []
    for palette in data['palettes']:
        details = [color_info(c) for c in palette['colors']]
        matches = details if target == 'any' else [c for c in details if target in c['tags']]
        if not matches:
            continue
        matches = [c for c in matches
                   if (lightness != 'light' or c['lightness'] >= .70)
                   and (lightness != 'dark' or c['lightness'] <= .45)
                   and (saturation != 'muted' or c['saturation'] <= .35)
                   and (saturation != 'vivid' or c['saturation'] >= .50)]
        if not matches:
            continue
        mean_lightness = sum(c['lightness'] for c in details)/3
        mean_saturation = sum(c['saturation'] for c in details)/3
        if lightness == 'light' and mean_lightness < .70:
            continue
        if lightness == 'dark' and mean_lightness > .45:
            continue
        if saturation == 'muted' and mean_saturation > .35:
            continue
        if saturation == 'vivid' and mean_saturation < .50:
            continue
        primary = max(matches, key=lambda c:c['chroma'])
        score = len(matches)*.4 + primary['chroma']*.6
        candidates.append((score, {'id':palette['id'], 'theme':families[palette['family']],
            'family':palette['family'], 'colors':palette['colors'], 'method':palette['method'],
            'image':palette.get('image'),
            'color_details':details, 'suggested_primary':primary['hex'],
            'matching_colors':[c['hex'] for c in matches],
            'mean_lightness':mean_lightness, 'mean_saturation':mean_saturation,
            'reason':f'Use {primary["name"]} {primary["hex"]} as primary; use the other colors for backgrounds or supporting elements'}))
    candidates.sort(key=lambda item:(-item[0], item[1]['id']))
    selected = []
    for distinct_family in (True, False):
        for _, candidate in candidates:
            if len(selected) >= limit:
                break
            if any(candidate['id'] == p['id'] for p in selected):
                continue
            if distinct_family and any(candidate['family'] == p['family'] for p in selected):
                continue
            # shortcut: RGB distance only removes near duplicates; use a validated color space for perceptual ranking.
            if any(palette_distance(candidate['colors'], p['colors']) < .08 for p in selected):
                continue
            selected.append(candidate)
    status = 'ok' if len(selected) == limit else 'fewer_matches' if selected else 'no_matches'
    return {'query':query, 'target':target, 'lightness':lightness, 'saturation':saturation,
            'requested':limit, 'returned':len(selected), 'status':status, 'results':selected,
            'note':'Only complete library palettes are returned; fewer matches are not padded with invented combinations. Primary colors and area ratios are application suggestions, not source annotations.'}
