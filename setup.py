#!/usr/bin/env python

from setuptools import setup


setup(
    install_requires=['distribute', 'Django<1.4'],
    name='django-supergeneric',
    version='0.1-dev',
    description='django-supergeneric is a small utility library that provides generic aggregator for five most used generic views for any model',
    author='Serge Matveenko',
    author_email='s@matveenko.ru',
    url='https://github.com/lig/django-supergeneric',
    packages=['supergeneric']
)
