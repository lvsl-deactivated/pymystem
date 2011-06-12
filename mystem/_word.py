# coding: utf-8

import mystem

class Word(object):
    def __init__(self, orig, lemmas_list=()):
        self.orig = orig
        self.parent_doc = None
        self.lemmas_list = lemmas_list
        self.lemmas = [mystem.Lemma(l[0], l[1], l[2]) for l in lemmas_list]

    def __eq__(self, other):
        if (isinstance(other, self.__class__) and
                other.orig == self.orig and
                other.lemmas == self.lemmas):
            return True
        else:
            return False

    def __contains__(self, item):
        return item in self.lemmas

    def __str__(self):
        return "<%s instance. Orig: %s. Lemmas: %s>" % (
            self.__class__.__name__,
            self.orig,
            ','.join(l[0] for l in self.lemmas_list)
        )

    def __repr__(self):
        return "<%s instance at %s. Orig: %s. Lemmas: %s>" % (
            self.__class__.__name__,
            hex(id(self)),
            self.orig,
            ','.join(l[0] for l in self.lemmas_list)
        )
