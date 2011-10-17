#!/usr/bin/env python
from distutils.core import setup

setup(
        name='samklang-pages',
        version="0.1.0",
	author='Sigurd Gartmann',
	author_email='sigurdga-samklang@sigurdga.no',
	url='http://github.com/sigurdga/samklang-pages',
	description='Pages module for Samklang',
	long_description=open('README.txt').read(),
	license="AGPL",
        packages=['samklang_pages', 'samklang_pages.migrations'],
        package_data={'samklang_pages': ['templates/samklang_pages/*.html', 'locale/*/LC_MESSAGES/django.*o']},
        py_modules=['samklang_pages.pagewidgets'],
	classifiers=[
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: GNU Affero General Public License v3",
		"Intended Audience :: Developers",
		"Framework :: Django",
		"Environment :: Web Environment",
		"Topic :: Internet :: WWW/HTTP :: Dynamic Content",
		]
        )
