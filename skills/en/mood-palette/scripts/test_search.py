"""Run with python3 scripts/test_search.py; standard library only."""
import unittest
import json
from pathlib import Path
from build_portable_search import catalog_fingerprint
from palette import catalog
from search import search, color_info, palette_distance


class SearchTests(unittest.TestCase):
    def test_portable_choices_match_live_search(self):
        data = catalog()
        index = json.loads((Path(__file__).resolve().parents[1] / 'references/portable-search.json').read_text())
        self.assertEqual(index['catalog_sha256'], catalog_fingerprint(data))
        self.assertEqual(len(index['conditions']), 117)
        for key, choices in index['conditions'].items():
            color, lightness, saturation = key.split('|')
            lightness = None if lightness == 'any' else lightness
            saturation = None if saturation == 'any' else saturation
            for limit in (1, 5, 10):
                live = search(data, color, limit, lightness, saturation)
                self.assertEqual(choices[:limit], [
                    {'id':p['id'], 'suggested_primary':p['suggested_primary']}
                    for p in live['results']], (key, limit))

    def test_basic_color_names(self):
        for value, tag in [('#0000FF','blue'),('#FFC0CB','pink'),('#FFFF00','yellow'),
                           ('#FFFFFF','white'),('#808080','gray'),('#000000','black')]:
            self.assertIn(tag, color_info(value)['tags'])
        self.assertNotIn('blue', color_info('#808080')['tags'])
        self.assertIn('purple', color_info('#9C8EC5')['tags'])
        self.assertNotIn('pink', color_info('#690021')['tags'])
        self.assertIn('green', color_info('#86A126')['tags'])
        self.assertEqual(color_info('#C0E3F5')['name'], 'light blue')

    def test_five_blue_choices_are_real_and_distinct(self):
        data = catalog(); found = search(data, 'blue', 5)
        originals = {p['id']:p['colors'] for p in data['palettes']}
        self.assertEqual(found['returned'], 5)
        self.assertEqual(len({p['family'] for p in found['results']}), 5)
        for p in found['results']:
            self.assertEqual(p['colors'], originals[p['id']])
            self.assertEqual(p['image'], f"assets/palettes/{p['id']}.png")
            self.assertIn('blue', color_info(p['suggested_primary'])['tags'])
        self.assertEqual([p['id'] for p in found['results']],
                         [p['id'] for p in search(data, '蓝色', 5)['results']])

    def test_filters_and_small_result_set(self):
        found = search(catalog(), 'pink', 5, lightness='light', saturation='muted')
        self.assertGreater(found['returned'], 0)
        for p in found['results']:
            self.assertGreaterEqual(p['mean_lightness'], .70)
            self.assertLessEqual(p['mean_saturation'], .35)
            self.assertTrue(any('pink' in c['tags'] for c in p['color_details']))
        data = catalog(); data['palettes'] = data['palettes'][:1]
        found = search(data, 'blue', 5)
        self.assertEqual(found['returned'], 1)
        self.assertEqual(found['status'], 'fewer_matches')
        self.assertEqual(search(data, 'pink', 5)['status'], 'no_matches')

    def test_order_and_compression_duplicates_are_removed(self):
        data = {'families':[{'id':'test','name':'Example'}], 'palettes':[
            {'id':'a','family':'test','colors':['#0000FF','#FFFFFF','#FFFF00'],'method':'printed_hex'},
            {'id':'b','family':'test','colors':['#FFFF00','#0000FE','#FFFFFF'],'method':'image_sample'}]}
        self.assertEqual(search(data, 'blue', 5)['returned'], 1)
        self.assertAlmostEqual(palette_distance(data['palettes'][0]['colors'],
                                               list(reversed(data['palettes'][0]['colors']))), 0)

    def test_light_blue_primary_is_actually_light(self):
        found = search(catalog(), 'blue', 5, lightness='light')
        self.assertGreater(found['returned'], 0)
        for p in found['results']:
            self.assertGreaterEqual(color_info(p['suggested_primary'])['lightness'], .70)
        data = {'families':[{'id':'test','name':'Example'}], 'palettes':[
            {'id':'a','family':'test','colors':['#0000FF','#FFFFFF','#FFFFEE'],'method':'printed_hex'}]}
        self.assertEqual(search(data, 'blue', lightness='light')['returned'], 0)

    def test_invalid_input(self):
        for args in [('not-a-color',5),('blue',0),('blue',101)]:
            with self.assertRaises(ValueError):search(catalog(), *args)


if __name__ == '__main__':
    unittest.main()
