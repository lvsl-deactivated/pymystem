# coding: utf-8

import re
import sys
import os.path

__all__ = ['MystemError', 'find_mystem', 'parse_mystem_out']

class MystemError(StandardError): pass

def find_mystem(path=None):
    bin_name = "mystem"
    if path:
        path_to_bin = path
    else:
        path_to_bin = os.path.join(
            os.path.join(
                os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))),
                "contrib"),
            bin_name)

    if not os.path.exists(path_to_bin):
        raise MystemError("Mystem binary not found at %s" % path_to_bin)

    return path_to_bin

def parse_mystem_out(s):
    '''\
    Parse -inf output
    '''
    parts = re.findall(r'([^{]+){([^}]+)}', s)
    if not parts:
        raise MystemError("Incorrect mystem output")
    res = {}
    for orig, info in parts:
        lemmas = re.split(r'\|(?!\=)', info)
        parsed_lemmas = []
        for l in lemmas:
            if '??' in l:
                form = l.replace('??', '')
                parsed_lemmas.append((form, None, None))
                continue
            lemma_parts = re.findall(r'^([^:]+):([\d.]+)=(.+)$', l)
            if not lemma_parts:
                raise MystemError("Incorrect mystem output")
            form, ipm, gr = lemma_parts[0]
            ipm = float(ipm)
            gr = gr.split('|=')
            parsed_gr = []
            for g in gr:
                g = g.replace('=', ',') # don't know what = is used for
                parsed_gr.append(g.split(','))
            parsed_lemmas.append((form, ipm, parsed_gr))
        orig = orig.strip()
        res[orig] = parsed_lemmas
    return res
