#!/usr/bin/env python
from setuptools import setup


setup(
    name="timecalc",
    version="0.1.6",
    description="a tool to make the imitation of Lyubishchev and his time billing method easier",
    author="Xin YUE",
    author_email="yuecn41@gmail.com",
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
