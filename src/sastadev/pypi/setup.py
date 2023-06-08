from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='sastadev',
    python_requires='>=3.7, <4',
    version='0.0.3',
    description='Linguistic functions for SASTA tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Digital Humanities Lab, Utrecht University',
    author_email='digitalhumanities@uu.nl',
    url='https://github.com/UUDigitalHumanitieslab/sastadev',
    license='BSD-3-Clause',
    include_package_data=True,
    packages=['sastadev'],
    package_data={
        'sastadev': ['*.txt', 'LICENSE', 'py.typed']
    }
)
