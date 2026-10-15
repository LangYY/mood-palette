"""Export deterministic palette choices for hosts without Python execution."""
import hashlib
import itertools
import json
from pathlib import Path

from search import ALIASES, search


def catalog_fingerprint(data):
    records = json.dumps(data['palettes'], sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(records.encode('utf-8')).hexdigest()


def build_index(data):
    conditions = {}
    for color, lightness, saturation in itertools.product(
            ALIASES, (None, 'light', 'dark'), (None, 'muted', 'vivid')):
        result = search(data, color, 100, lightness, saturation)
        key = '|'.join((color, lightness or 'any', saturation or 'any'))
        conditions[key] = [{'id':p['id'], 'suggested_primary':p['suggested_primary']}
                           for p in result['results']]
    return {'version':1, 'catalog_sha256':catalog_fingerprint(data),
            'key_format':'color|lightness-or-any|saturation-or-any',
            'conditions':conditions}


if __name__ == '__main__':
    references = Path(__file__).resolve().parents[1] / 'references'
    data = json.loads((references/'palettes.json').read_text())
    index = build_index(data)
    assert len(index['conditions']) == 117
    (references/'portable-search.json').write_text(json.dumps(index, indent=2)+'\n')
    print('Exported 117 portable search conditions from the catalog.')
