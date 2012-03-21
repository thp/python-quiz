#!/bin/sh

set -e

sh profile_scripts.sh ../*.py
python convert_stats.py *.prof
python summary.py *.stats -csv > summary.csv
python summary.py *.stats

