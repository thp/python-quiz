
import pstats
import sys
import os

for arg in sys.argv[1:]:
    basename, _ = os.path.splitext(os.path.basename(arg))
    outfile = open(basename + '.stats', 'w')
    p = pstats.Stats(arg, stream=outfile)
    p.sort_stats('time', 'cum').print_stats()
    outfile.close()

