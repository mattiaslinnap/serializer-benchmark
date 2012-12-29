#!/usr/bin/env python

from collections import defaultdict
import gzip
import msgpack
import os
from os.path import join as j
import shutil
import struct
import sys
import time
import ujson

import parser


class Packer(object):
    def write(self, datadir, subdir, filename, objects):
        outdir = j(self.basedir(datadir), subdir)
        try:
            os.makedirs(outdir)
        except OSError:
            pass
        f = self.openfile(j(outdir, filename))
        try:
            for obj in objects:
                f.write(self.pack(obj))
        finally:
            f.close()

    def basedir(self, datadir):
        return j(datadir, str(self))

    def openfile(self, fullfilename):
        return open(fullfilename, 'wb')

class JsonPacker(Packer):
    def pack(self, obj):
        line = ujson.dumps(obj)
        return '\0' + struct.pack('>i', len(line)) + line + '\n'
    def __str__(self):
        return 'json'

class MsgpackPacker(Packer):
    def pack(self, obj):
        return msgpack.dumps(obj)
    def __str__(self):
        return 'msgpack'

class GzipJsonPacker(JsonPacker):
    def openfile(self, fullfilename):
        return gzip.open(fullfilename + '.gz', 'wb')
    def __str__(self):
        return 'gzipjson'

class GzipMsgpackPacker(MsgpackPacker):
    def openfile(self, fullfilename):
        return gzip.open(fullfilename + '.gz', 'wb')
    def __str__(self):
        return 'gzipmsgpack'


def write_objects(datadir, subdir, objects, packer, gzip):
    dirname = j(datadir, packer, subdir)
    filename = j(dirname)
    os.makedirs()


def main(datadir):
    times = defaultdict(float)
    packers = [JsonPacker(), MsgpackPacker(), GzipJsonPacker(), GzipMsgpackPacker()]
    for packer in packers:
        shutil.rmtree(packer.basedir(datadir), ignore_errors=True)

    for i, (subdir, filename, objects) in enumerate(parser.parsefiles(j(datadir, 'pserver-uploads'))):
        for packer in packers:
            start = time.time()
            packer.write(datadir, subdir, filename, objects)
            times[str(packer)] += (time.time() - start)
        if i % 100 == 0:
            print >> sys.stderr, '%d processed' % i

    for key, val in times.iteritems():
        print '%s: %.3f seconds' % (key, val)


if __name__ == '__main__':
    main(sys.argv[1])
