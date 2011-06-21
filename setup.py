#!/usr/bin/env python
from distutils.core import setup

setup(
        name = 's7n-pages',
        version = "1a1",
        packages = ['s7n.pages'],
        package_data = {'s7n.pages': ['templates/pages/*.html']},
        )
