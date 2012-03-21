
import re
import sys

stats_re = r'(\d+) function calls.*in ([0-9.]+) seconds'

use_csv = ('-csv' in sys.argv)
if use_csv:
    sys.argv.remove('-csv')
    print 'Filename;Time (Seconds);Calls'

stats = []
for filename in sys.argv[1:]:
    d = open(filename).read()
    calls, seconds = map(float, re.search(stats_re, d).groups())
    stats.append((seconds, calls, filename))

stats.sort()

for stat in stats:
    if use_csv:
        print '%s;%f;%d' % (stat[2], stat[0], stat[1])
    else:
        print '   %10.3fs  %10d calls     %s' % stat
