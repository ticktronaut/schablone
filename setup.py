#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import schablone

setup(
    name='schablone',
    version=schablone.__version__,
    description='Create labels of different types and render them to svg.',
    long_description='schablone is a library to create structured printed forms (svg format) and fill them with information.',
    author='Andreas Gschossmann',
    author_email='ghandi_84@hotmail.com',
    url='http://github.com/ticktronaut/schablone',
    license='MIT',
    install_requires=['lxml', 'svglue>=0.2.2.dev1', 'svgutils', 'pyqrcode', 'pystrich', 'warnings'],
    include_package_data=True,
    packages=find_packages(exclude=('docs'))
)
