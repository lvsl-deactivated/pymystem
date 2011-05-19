# coding: utf-8

import os.path
import unittest
import lib.util

class UtilTests(unittest.TestCase):
    def test_find_mystem(self):
        path = lib.util.find_mystem()
        self.assertTrue(os.path.exists(path))

    def test_bad_path(self):
        self.assertRaises(lib.util.MystemError,
                          lib.util.find_mystem,
                          "/non-existing-file")

    def test_parse_mystem_out(self):
        sample_out = (
            "Мама{мама:313.80=S,жен,од=им,ед}\n"
            "мыла{мыть:26.70=V,несов=прош,ед,изъяв,жен,пе|мыло:16.30=S,сред,неод=им,мн|=S,сред,неод=род,ед|=S,сред,неод=вин,мн}\n"
            "huge{huge??}\n"
            "раму{рама:22.50=S,жен,неод=вин,ед|рам:0.00=S,гео,муж,неод=дат,ед}\n"
        )
        r = lib.util.parse_mystem_out(sample_out)
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


def suite():
    loader = unittest.TestLoader()
    return unittest.TestSuite([
        loader.loadTestsFromTestCase(UtilTests)
    ])
