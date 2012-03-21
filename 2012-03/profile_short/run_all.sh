#!/bin/sh

set -e

if [ $# -eq 0 ]; then
    FILES=../*.py
else
    FILES="$*"
fi

sh profile_scripts.sh $FILES
python convert_stats.py *.prof
python summary.py *.stats -csv > summary.csv
python summary.py *.stats

