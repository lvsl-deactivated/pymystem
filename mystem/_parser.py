# coding: utf-8

#
# Mystem class
#

import util

__all__ = ['Mystem']

class Parser(object):
    def __init__(self):
    '''\
    Wrapper for myste -inf command
    '''
        self._mystem_file = util.find_mystem()
        self._mystem_opts = ["-inf", "-e", "utf-8"]
        self._pool = None

    def start(self, workers=1):
        pass

    def stop(self):
        pass

    def parse(self):
        pass
