#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import schablone

setup(
    name='schablone',
    version=schablone.__version__,
    description='Create labels of different types and render them to svg.',
    long_description='tbc',
    author='Andreas Gschossmann',
    author_email='ghandi_84@hotmail.com',
    url='http://github.com/ticktronaut/schablone',
    license='MIT',
    install_requires=['lxml', 'svglue', 'svgutils', 'pyqrcode'], # FixMe: gi for virtualenvs?
    packages=find_packages(exclude=('docs'))
)
