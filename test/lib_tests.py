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

    def test_grammeme_str(self):
        g1 = mystem.Grammeme('S', 'гео', 'муж', 'неод', 'дат', 'ед')
        self.assertEqual(str(g1), "<Grammeme instance. Tag: S. OTHER: 'гео'. GENDER: 'муж'. ANINIMATION: 'неод'. CASE: 'дат'. NUMBER: 'ед'>")

    def test_lemma_ctor1(self):
        l = mystem.Lemma('мыло',
                         16.3,
                         [['S', 'сред', 'неод', 'им', 'мн'],
                          ['S', 'сред', 'неод', 'род', 'ед'],
                          ['S', 'сред', 'неод', 'вин', 'мн']])

        self.assertEqual(l.lemma, 'мыло')
        self.assertEqual(l.ipc, 16.3)
        self.assertEqual(l.grammems, (
            mystem.Grammeme('S', 'сред', 'неод', 'им', 'мн'),
            mystem.Grammeme('S', 'сред', 'неод', 'род', 'ед'),
            mystem.Grammeme('S', 'сред', 'неод', 'вин', 'мн'),
        ))

    def test_lemma_str(self):
        l = mystem.Lemma('мыло',
                         16.3,
                         [['S', 'сред', 'неод', 'им', 'мн'],
                          ['S', 'сред', 'неод', 'род', 'ед'],
                          ['S', 'сред', 'неод', 'вин', 'мн']])
        self.assertEqual(str(l), '<Lemma instance. Lemma: мыло. Grammar: S,сред,неод,им,мн|=S,сред,неод,род,ед|=S,сред,неод,вин,мн>')

    def test_lemma_eq(self):
        l1 = mystem.Lemma('мыло',
                         16.3,
                         [['S', 'сред', 'неод', 'им', 'мн'],
                          ['S', 'сред', 'неод', 'род', 'ед'],
                          ['S', 'сред', 'неод', 'вин', 'мн']])
        l2 = mystem.Lemma('мыло',
                         16.1,
                         [['S', 'сред', 'неод', 'им', 'мн'],
                          ['S', 'сред', 'неод', 'род', 'ед'],
                          ['S', 'сред', 'неод', 'вин', 'мн']])
        l3 = mystem.Lemma('мыло',
                         16.3,
                         [['V', 'сред', 'неод', 'им', 'мн'],
                          ['S', 'сред', 'неод', 'род', 'ед'],
                          ['S', 'сред', 'неод', 'вин', 'мн']])
        l4 = mystem.Lemma('мылож',
                         16.3,
                         [['V', 'сред', 'неод', 'им', 'мн'],
                          ['S', 'сред', 'неод', 'род', 'ед'],
                          ['S', 'сред', 'неод', 'вин', 'мн']])

        self.assertEqual(l1, l2)
        self.assertEqual(l2, l2)
        self.assertNotEqual(l2, l3)
        self.assertNotEqual(l3, l4)

    def test_lemma_contain(self):
        l1 = mystem.Lemma('мыло',
                         16.3,
                         [['S', 'сред', 'неод', 'им', 'мн'],
                          ['S', 'сред', 'неод', 'род', 'ед'],
                          ['S', 'сред', 'неод', 'вин', 'мн']])
        g1 = mystem.Grammeme('S', 'сред', 'неод', 'им', 'мн')
        self.assertTrue(g1 in l1)

    def test_word_ctor(self):
        r = ('мыла', [('мыть',
                      26.7,
                      [['V', 'несов', 'прош', 'ед', 'изъяв', 'жен', 'пе']]),
                     ('мыло',
                      16.3,
                      [['S', 'сред', 'неод', 'им', 'мн'],
                       ['S', 'сред', 'неод', 'род', 'ед'],
                       ['S', 'сред', 'неод', 'вин', 'мн']])])
        w = mystem.Word(r[0], r[1])
        self.assertEqual(w.orig, 'мыла')

    def test_word_eq(self):
        r1 = ('мыла', [('мыть',
                      26.7,
                      [['V', 'несов', 'прош', 'ед', 'изъяв', 'жен', 'пе']]),
                     ('мыло',
                      16.3,
                      [['S', 'сред', 'неод', 'им', 'мн'],
                       ['S', 'сред', 'неод', 'род', 'ед'],
                       ['S', 'сред', 'неод', 'вин', 'мн']])])
        w1 = mystem.Word(r1[0], r1[1])
        r2 = ('мыла', [('мыть',
                      26.7,
                      [['V', 'несов', 'прош', 'ед', 'изъяв', 'жен', 'пе']]),
                     ('мыло',
                      16.3,
                      [['S', 'сред', 'неод', 'им', 'мн'],
                       ['S', 'сред', 'неод', 'род', 'ед'],
                       ['S', 'сред', 'неод', 'вин', 'мн']])])
        w2 = mystem.Word(r2[0], r2[1])
        self.assertEqual(w1, w2)

    def test_word_in(self):
        r1 = ('мыла', [('мыть',
                      26.7,
                      [['V', 'несов', 'прош', 'ед', 'изъяв', 'жен', 'пе']]),
                     ('мыло',
                      16.3,
                      [['S', 'сред', 'неод', 'им', 'мн'],
                       ['S', 'сред', 'неод', 'род', 'ед'],
                       ['S', 'сред', 'неод', 'вин', 'мн']])])
        w1 = mystem.Word(r1[0], r1[1])
        l1 = mystem.Lemma('мыло',
                         16.3,
                         [['S', 'сред', 'неод', 'им', 'мн'],
                          ['S', 'сред', 'неод', 'род', 'ед'],
                          ['S', 'сред', 'неод', 'вин', 'мн']])
        self.assertTrue(l1 in w1)

    def test_word_str(self):
        r1 = ('мыла', [('мыть',
                      26.7,
                      [['V', 'несов', 'прош', 'ед', 'изъяв', 'жен', 'пе']]),
                     ('мыло',
                      16.3,
                      [['S', 'сред', 'неод', 'им', 'мн'],
                       ['S', 'сред', 'неод', 'род', 'ед'],
                       ['S', 'сред', 'неод', 'вин', 'мн']])])
        w1 = mystem.Word(r1[0], r1[1])
        self.assertEqual(str(w1), '<Word instance. Orig: мыла. Lemmas: мыть,мыло>')

    def test_document_ctor(self):
        words_dict = {
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

        text = "huge Мама мыла раму"

        doc = mystem.Document(1, text, words_dict)
        self.assertEqual(doc.docid, 1)
        self.assertEqual(doc.text, text)

    def test_document_str(self):
        words_dict = {
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

        text = "huge Мама мыла раму"

        doc = mystem.Document(1, text, words_dict)
        self.assertEqual(str(doc), '<Document instance. docid: 1>')

    def test_document_len(self):
        words_dict = {
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

        text = "huge Мама мыла раму"

        doc = mystem.Document(1, text, words_dict)
        self.assertEqual(len(doc), 4)

    def test_document_in(self):
        words_dict = {
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

        text = "huge Мама мыла раму"

        doc = mystem.Document(1, text, words_dict)
        r1 = ('мыла', [('мыть',
                      26.7,
                      [['V', 'несов', 'прош', 'ед', 'изъяв', 'жен', 'пе']]),
                     ('мыло',
                      16.3,
                      [['S', 'сред', 'неод', 'им', 'мн'],
                       ['S', 'сред', 'неод', 'род', 'ед'],
                       ['S', 'сред', 'неод', 'вин', 'мн']])])
        w1 = mystem.Word(r1[0], r1[1])
        self.assertTrue(w1 in doc)


def suite():
    loader = unittest.TestLoader()
    return unittest.TestSuite([
        loader.loadTestsFromTestCase(UtilTests)
    ])
