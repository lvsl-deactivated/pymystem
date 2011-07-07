# coding: utf-8

import os
import md5
import subprocess

import mystem

class Parser(object):
    @classmethod
    def parse(cls, text):
        if os.getenv('MYSTEM_PATH'):
            mystem_path = os.getenv('MYSTEM_PATH')
        else:
            mystem_path = mystem.util.find_mystem()
        p = subprocess.Popen([mystem_path, '-e', 'utf-8', '-inf'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate(input=text)
        if p.returncode:
            raise mystem.util.MystemError("mystem returned: %s" % p.returncode)

        parsed_out = mystem.util.parse_mystem_out(out)
        docid = md5.md5(text).hexdigest()

        doc = mystem.Document(docid, text, parsed_out)

        return doc

