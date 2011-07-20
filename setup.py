#!/usr/bin/env python
from distutils.core import setup

setup(
        name = 's7n-pages',
        version = "1a1",
        packages = ['s7n', 's7n.pages', 's7n.pages.migrations'],
        package_data = {'s7n.pages': ['templates/pages/*.html', 'locale/*/LC_MESSAGES/django.*o']},
        py_modules = ['s7n.pages.pagewidgets'],
        )
