
import re
import sys
import os

stats_re = r'(\d+) function calls.*in ([0-9.]+) seconds'

def getlines(filename):
    return len(open(filename).read().splitlines())

def getchars(filename):
    return len(open(filename).read())

use_csv = ('-csv' in sys.argv)
if use_csv:
    sys.argv.remove('-csv')
    print 'Filename;Time (Seconds);Calls;Lines;Chars'

stats = []
for filename in sys.argv[1:]:
    d = open(filename).read()
    calls, seconds = map(float, re.search(stats_re, d).groups())
    stats.append((seconds, calls, filename))

stats.sort()

for stat in stats:
    if use_csv:
        filename = '../%s.py' % (os.path.splitext(stat[2])[0])
        lines = getlines(filename)
        chars = getchars(filename)
        print '%s;%f;%d;%d;%d' % (stat[2], stat[0], stat[1], lines, chars)
    else:
        print '   %10.3fs  %10d calls     %s' % stat
