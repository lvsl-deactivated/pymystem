#!/usr/bin/env python
import sys
import time
import tempfile
import subprocess

from lib import util

def mystem(args, fin=sys.stdin, fout=sys.stdout, ferr=sys.stderr, input_data=None):
    '''\
    Generic wrapper for MyStem
    '''
    mystem_path = util.find_mystem()

    # make utf-8 a default encoding
    if '-e' not in args:
        args.extend(["-e", "utf-8"])

    p = subprocess.Popen([mystem_path] + args,
                         stdout=fout,
                         stderr=ferr,
                         stdin=fin)

    out_data, err_data = p.communicate(input=input_data)

    return p.returncode, out_data, err_data


def main(args):
    return mystem(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:])[0])
