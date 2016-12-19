#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='label',
    version='0.2dev',
    description='Create labels of different types and render them to svg.',
    long_description='tbc',
    author='Andreas Gschossmann',
    author_email='ghandi_84@hotmail.com',
    url='http://github.com/ticktronaut/label',
    license='MIT',
    install_requires=['lxml', 'svglue', 'os', 'pyqrcode'],
    packages=find_packages(exclude=('docs'))
)
