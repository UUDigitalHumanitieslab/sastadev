#!/usr/bin/env bash
find sastadev/ -type f -not -name '.gitignore' -delete
TARGET=$PWD/../pypi/sastadev/
cp config.py $TARGET
cd ..
cp LICENSE __init__.py deregularise.py inflectioncorrection.tsv.txt $TARGET

cd pypi
python setup.py sdist
