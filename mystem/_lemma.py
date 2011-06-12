# coding: utf-8

import mystem

class Lemma(object):
    def __init__(self, lemma, ipc=None, gr_list=(), parent_word=None):
        self.lemma = lemma
        self.ipc = float(ipc)
        self.parent_word = parent_word
        self.gr_list = gr_list
        self.grammems = tuple(mystem.Grammeme(*gr) for gr in gr_list)

    def is_bound_to_word(self):
        return self.parent_word is not None

    def gr_list2str(self):
        return '|='.join(','.join(g) for g in self.gr_list)

    def __str__(self):
        return '<%s instance. Lemma: %s. Grammar: %s>' % (
            self.__class__.__name__,
            self.lemma,
            self.gr_list2str(),
        )

    def __repr__(self):
        return '<%s instance at %s. Lemma: %s. Grammar: %s>' % (
            self.__class__.__name__,
            hex(id(self)),
            self.lemma,
            self.gr_list2str(),
        )

    def __eq__(self, other):
        if (isinstance(other, self.__class__) and
                other.lemma == self.lemma and
                other.grammems == self.grammems):
            return True
        else:
            return False

    def __contains__(self, item):
        return item in self.grammems



