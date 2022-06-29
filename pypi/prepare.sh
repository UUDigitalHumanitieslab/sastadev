#!/usr/bin/env bash
find sastadev/ -type f -not -name '.gitignore' -delete
TARGET=$PWD/../pypi/sastadev/
cp __config__.py $TARGET/config.py
cd ..
cp LICENSE __init__.py deregularise.py inflectioncorrection.tsv.txt py.typed $TARGET

cd pypi
python setup.py sdist
