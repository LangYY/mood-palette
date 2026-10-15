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
NAMES = dict(blue='蓝色', pink='粉红色', yellow='黄色', red='红色', orange='橙色',
             green='绿色', cyan='青色', purple='紫色', brown='棕色', white='白色',
             gray='灰色', black='黑色')


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
        name = ('浅灰色' if lightness >= .75 else '深灰色' if lightness <= .35 else '灰色') if family == 'gray' else NAMES[family]
    elif lightness > .88 and max(rgb) - min(rgb) < .25:
        name = '米白色' if hue < 65 else {'blue':'蓝白色', 'cyan':'青白色', 'green':'绿白色',
                                           'purple':'紫白色', 'pink':'粉白色', 'red':'粉白色'}[family]
        tags.append('white')
    elif saturation < .18 or (lightness < .35 and saturation < .25):
        name = {'blue':'蓝灰色', 'cyan':'青灰色', 'purple':'紫灰色', 'pink':'粉灰色',
                'yellow':'暖灰色', 'orange':'暖灰色', 'red':'暖灰色'}.get(family, '灰绿色')
        tags.append('gray')
    else:
        prefix = '浅' if lightness >= .72 or (saturation < .35 and lightness >= .55) else '深' if lightness <= .35 else ''
        name = prefix + ('黄绿色' if family == 'green' and hue < 85 else NAMES[family])
    return {'hex': hex_color, 'name': name, 'tags': tags,
            'lightness': lightness, 'saturation': saturation, 'chroma':max(rgb)-min(rgb)}


def palette_distance(a, b):
    def rgb(color):
        return tuple(int(color[i:i+2], 16)/255 for i in (1, 3, 5))
    return min(sum(dist(rgb(x), rgb(y)) for x, y in zip(a, order))/3
               for order in permutations(b))


def search(data, query, limit=5, lightness=None, saturation=None):
    if not 1 <= limit <= 100:
        raise ValueError('推荐数量须为 1–100')
    target = next((key for key, words in ALIASES.items() if query.strip().lower() in words), None)
    if target is None:
        raise ValueError('请使用基本颜色名（如蓝色、粉红色）或 any；明度与饱和度使用对应选项')
    if lightness not in (None, 'light', 'dark') or saturation not in (None, 'muted', 'vivid'):
        raise ValueError('不支持的明度或饱和度条件')
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
            'reason':f'可将{primary["name"]} {primary["hex"]} 作为主色，其余两色作背景或辅助色'}))
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
            # shortcut: RGB 距离只用于去除近似重复，需感知色差排序时换用经验证的色彩空间。
            if any(palette_distance(candidate['colors'], p['colors']) < .08 for p in selected):
                continue
            selected.append(candidate)
    status = 'ok' if len(selected) == limit else 'fewer_matches' if selected else 'no_matches'
    return {'query':query, 'target':target, 'lightness':lightness, 'saturation':saturation,
            'requested':limit, 'returned':len(selected), 'status':status, 'results':selected,
            'note':'仅推荐库内完整色组；去除近似重复后不足指定数量时不补造。主色和面积是应用建议，原记录未标注比例。'}
