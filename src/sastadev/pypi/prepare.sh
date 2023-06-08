#!/usr/bin/env bash
find sastadev/ -type f -not -name '.gitignore' -delete
TARGET=$PWD/../pypi/sastadev/
cp __config__.py $TARGET/config.py

while read SOURCE
do
    cp -r ../$SOURCE $TARGET
done < include.txt

python setup.py sdist
