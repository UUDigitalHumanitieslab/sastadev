# Sastadev

[![Actions Status](https://github.com/UUDigitalHumanitieslab/sastadev/workflows/Unit%20tests/badge.svg)](https://github.com/UUDigitalHumanitieslab/sastadev/actions)

[pypi sastadev](https://pypi.org/project/sastadev)

Method definitions for use in SASTA

## Installation
You can install SASTADEV using pip:
```
pip install auchann
```

## Usage
The installation provides an entrypoint `sastadev` which invokes `sastadev.__main__.main()`

To lists arguments and options:

```
sastadev -h
```
or
```
python -m sastadev -h
```

## Configuration
TODO

## Development
To install the requirements:
```
pip install -r requirements.txt
```

### Testing
Tests should be written and run using [pytest](https://docs.pytest.org/).
To test, make sure the package is installed in editable mode:
```
pip install -e .
```

Then, each time you wis to run the tests:
```
pytest
```

### Linting
Linting configuration is provided for [flake8](https://flake8.pycqa.org/en/latest/).
To lint, run:
```
flake8 ./src/sastadev/
```

### Upload to PyPi

Specify the files which should be included in the package in `pypi/include.txt`.

```bash
cd pypi
./prepare.sh
twine upload dist/*
```
