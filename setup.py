#!/usr/bin/env python
from setuptools import setup


setup(
    name="timecalc",
    version="0.1.0",
    description="a tool to summarize your bills of time",
    url="https://github.com/yuex/timecalc",
    package_dir={'': 'src'},
    py_modules=['timecalc'],
    install_requires=[
        "PyYAML==3.11",
    ],
    entry_points={
        'console_scripts': ['timecalc=timecalc:main'],
    },
)
