#!/usr/bin/env python3

from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'pandas', 'click', 'loguru', 'pytest', 'pytest-xdist',
    'holidays', 'numpy', 'pytz', 'psutil', 'emoji',
    'deep-translator', 'sqlalchemy', 'setuptools',
    'regex', 'dateparser', 'pymysql'
]

PACKAGE_NAME = 'google_maps_travel_time_monitor'
EMAIL = ""
DESCRIPTION = ""
LICENSE = ""
CONSOLE_SCRIPTS = [
    "gmttm=google_maps_travel_time_monitor.app:main"
]


def __get_version():
    with open(f'{PACKAGE_NAME}/__init__.py') as f:
        info = {}
        for line in f:
            if line.startswith('__version__'):
                exec(line, info)
                break
    return info['__version__']


setup(
    name=PACKAGE_NAME.replace('_', '-'),
    version=__get_version(),
    author=EMAIL,
    author_email=EMAIL,
    description=DESCRIPTION,
    packages=find_packages(exclude=['*.tests']),
    license=LICENSE,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': CONSOLE_SCRIPTS
    },
    python_requires='>=3.9',
)
