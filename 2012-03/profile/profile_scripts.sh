#!/bin/sh

set -e

INFILE=perftest.txt

for file in $*; do
    echo "`date` $file"
    python -m cProfile -o `basename $file .py`.prof $file $INFILE >/dev/null
done

