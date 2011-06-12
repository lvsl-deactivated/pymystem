# coding: utf-8
import copy

import mystem

class Document(object):
    def __init__(self, docid=None, text='', word_dict=None):
        self.docid = docid or id(self)
        self.text = text
        self.word_dict = copy.deepcopy(word_dict) if word_dict else  {}
        self.words = [mystem.Word(orig, lemmas) for orig, lemmas in self.word_dict.items()]

    def __str__(self):
        return "<%s instance. docid: %s>" % (
            self.__class__.__name__,
            self.docid
        )

    def __repr__(self):
        return "<%s instance at %s. docid: %s>" % (
            self.__class__.__name__,
            hex(id(self)),
            self.docid
        )

    def __len__(self):
        return len(self.word_dict)

    def __contains__(self, item):
        return item in self.words

