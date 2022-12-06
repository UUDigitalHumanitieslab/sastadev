# Sastadev

[![Actions Status](https://github.com/UUDigitalHumanitieslab/sastadev/workflows/Unit%20tests/badge.svg)](https://github.com/UUDigitalHumanitieslab/sastadev/actions)

[pypi sastadev](https://pypi.org/project/sastadev)

Method definitions for use in SASTA

Copy `default_config.py` to your own `config.py` in the `sastadev` directory, and change what you need.

## Upload to PyPi

Specify the files which should be included in the package in `pypi/include.txt`.

```bash
cd pypi
./prepare.sh
twine upload dist/*
```
