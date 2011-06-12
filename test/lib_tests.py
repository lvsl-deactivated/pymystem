# coding: utf-8

import os.path
import unittest

import mystem

class UtilTests(unittest.TestCase):
    def test_find_mystem(self):
        path = mystem.util.find_mystem()
        self.assertTrue(os.path.exists(path))

    def test_bad_path(self):
        self.assertRaises(mystem.util.MystemError,
                          mystem.util.find_mystem,
                          "/non-existing-file")

    def test_parse_mystem_out(self):
        sample_out = (
            "Мама{мама:313.80=S,жен,од=им,ед}\n"
            "мыла{мыть:26.70=V,несов=прош,ед,изъяв,жен,пе|мыло:16.30=S,сред,неод=им,мн|=S,сред,неод=род,ед|=S,сред,неод=вин,мн}\n"
            "huge{huge??}\n"
            "раму{рама:22.50=S,жен,неод=вин,ед|рам:0.00=S,гео,муж,неод=дат,ед}\n"
        )
        r = mystem.util.parse_mystem_out(sample_out)
        res = {
            'huge': [('huge', None, None)],
            'Мама': [('мама', 313.8, [['S', 'жен', 'од', 'им', 'ед']])],
            'мыла': [('мыть',
                      26.7,
                      [['V', 'несов', 'прош', 'ед', 'изъяв', 'жен', 'пе']]),
                     ('мыло',
                      16.3,
                      [['S', 'сред', 'неод', 'им', 'мн'],
                       ['S', 'сред', 'неод', 'род', 'ед'],
                       ['S', 'сред', 'неод', 'вин', 'мн']])],
            'раму': [('рама', 22.5, [['S', 'жен', 'неод', 'вин', 'ед']]),
                     ('рам', 0.0, [['S', 'гео', 'муж', 'неод', 'дат', 'ед']])]}
        self.assertEqual(r, res)

    def test_grammeme_class_ctor1(self):
        g1 = mystem.Grammeme('S', 'гео', 'муж', 'неод', 'дат', 'ед')
        self.assertEqual(g1.tag, 'S')

    def test_grammeme_class_ctor2(self):
        g1 = mystem.Grammeme('S')
        self.assertEqual(g1.tag, 'S')

    def test_bad_grammeme_class_ctor(self):
        self.assertRaises(mystem.util.MystemError,
                          lambda: mystem.Grammeme('S', ['гео']))

    def test_bad_grammeme_class_ctor2(self):
        self.assertRaises(mystem.util.MystemError,
                          lambda: mystem.Grammeme('S', ''))

    def test_bad_grammeme_class_ctor3(self):
        self.assertRaises(mystem.util.MystemError,
                          lambda: mystem.Grammeme('S', 'foo'))

    def test_grammeme_eq(self):
        g1 = mystem.Grammeme('S', 'гео', 'муж', 'неод', 'дат', 'ед')
        g2 = mystem.Grammeme('S', 'сред', 'неод', 'им', 'мн')
        g3 = mystem.Grammeme('S', 'гео', 'муж', 'неод', 'дат', 'ед')

        self.assertNotEqual(g1, g2)
        self.assertEqual(g1, g3)
        self.assertEqual(g2, g2)
        self.assertNotEqual(g2, g3)

    def test_grammeme_in(self):
        g1 = mystem.Grammeme('S', 'гео', 'муж', 'неод', 'дат', 'ед')

        self.assertTrue('гео' in g1)
        self.assertFalse('foo' in g1)

    def test_grammeme_parent(self):
        g1 = mystem.Grammeme('S', 'гео', 'муж', 'неод', 'дат', 'ед')
        self.assertFalse(g1.is_bound_to_lemma)

def suite():
    loader = unittest.TestLoader()
    return unittest.TestSuite([
        loader.loadTestsFromTestCase(UtilTests)
    ])
