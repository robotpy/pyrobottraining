#!/bin/bash

MAXTESTS=5

if [ "$1" == "" ]; then
    echo "Usage: ./run_single.sh TEST_NUMBER"
    exit 1
fi


TESTNAME=test_challenges.py::test_$1
shift

cd `dirname $0`
python3 robot.py test -- -l "$@" $TESTNAME
