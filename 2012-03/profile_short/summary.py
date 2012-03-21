
import re
import sys

stats_re = r'(\d+) function calls .(\d+) primitive calls. in ([0-9.]+) seconds'

use_csv = ('-csv' in sys.argv)
if use_csv:
    sys.argv.remove('-csv')
    print 'Filename;Calls'

stats = []
for filename in sys.argv[1:]:
    d = open(filename).read()
    calls, primitive, seconds = map(float, re.search(stats_re, d).groups())
    stats.append((calls, seconds, primitive, filename))

stats.sort()

for stat in stats:
    if use_csv:
        print '%s;%d' % (stat[3], stat[0])
    else:
        stat = stat[1], stat[0], stat[2], stat[3]
        print '   %10.3fs  %10d (%10d) calls     %s' % stat
