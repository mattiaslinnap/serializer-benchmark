"""Source data parser for benchmarks."""

from __future__ import absolute_import, division, print_function, unicode_literals

import gzip
import os
from os.path import join as j
import ujson
import sys


def objects(filename):
    errorlines = []
    with gzip.open(filename) as f:
        for i, line in enumerate(f.read().split('\x00A\x00b\x00b\x00a\x00')):
            line = line.strip()
            if line:
                try:
                    yield ujson.loads(line)
                except ValueError:
                    errorlines.append(i)
        if errorlines:
            if len(errorlines) > 1 or errorlines[0] != i:
                print('Errors on lines {0} of {1}'.format(errorlines, i), file=sys.stderr)

def parsefiles(datadir):
    for installid in os.listdir(datadir):
        for queue in os.listdir(j(datadir, installid)):
            for date in os.listdir(j(datadir, installid, queue)):
                subdir = j(installid, queue, date)
                for filename in os.listdir(j(datadir, subdir)):
                    fullfilename = j(datadir, subdir, filename)
                    yield subdir, filename.replace('.gz', ''), list(objects(fullfilename))
                return
