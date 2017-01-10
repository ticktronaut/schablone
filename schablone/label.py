#!/usr/bin/env python
#coding=utf-8

#import svgutils
import svgutils.transform as sg
import svglue
#import svgwrite
#import pysvg

from lxml import etree

#import warnings
import os

#import pyqrcode

import pkg_resources

import uuid
from pystrich.datamatrix import DataMatrixEncoder

#from .base import
from .generic import *


class smd_content_container(object):
    def __init__(self):
        self.title = ''
        self.value = ''
        self.package = ''
        self.tolerance = ''
        self.temperature_coefficient = ''
        self.power = ''
        self.tmpl_path = 'templates/label/smd_container/'


class smd_container(generic):
    def __init__(self):
        super(smd_container, self).__init__()

        #self.qr_content = "http://www.sappz.de"

        self.content = smd_content_container()

        self.label_type = "mira_1"  #todo: link zu quelle #getter setter: remove all layers, reset layers
        self.cut = False  #todo getter setter: remove all layers, reset layers
        #self.__cut_list = []

        self.cpt_tspan = {
            'title': '',
            'value': '',
            'package': '',
            'tolerance': '',
            'temperature_coefficient': '',
            'power': ''
        }
        #		self.cpt_flowpara = {}
        self.cpt_rect = {'matrix': ''}
        # todo: self.cut_list

    # hier wird die einzige Moeglichkeit der Basisklasse 
    # die Hoehe und Breite zu setzen ueberschrieben
    # Achtung ist überschreibend
    def save(self, fn=None):

        # set width and height (reconfigure everytime time save is called)
        self.width = '15mm'
        if self.label_type == 'mira_1' or 'mira_1a':  # type "1" and type "1a" seem to have label same size
            self.width = '15mm'
            self.height = '20mm'
        elif self.label_type == 'mira_2':
            raise RuntimeError('Label type mira_2 not supported, yet.')
        elif self.label_type == 'mira_3':
            raise RuntimeError('Label type mira_3 not supported, yet.')
        elif self.label_type == "mira_4":
            raise RuntimeError('Label type mira_4 not supported, yet.')
        else:
            raise RuntimeError('Unknown type of label: ' + self.label_type)

        # self.fn is set after this point 
        # todo: think about better solution for self._fn (explicit is better than implicit) 
        super(smd_container, self).save_frame(fn)

#        # save data matrix code with unique id (using bash)
#        fn, fext = os.path.splitext(self._fn)
#        fn_qr = fn + '_qr' + '.png'
#        os.system(
#            'uuidgen | tr [[:upper:]] [[:lower:]] | tr -d \'-\'  | sed -e \'s/\(.\{12\}\).*/\\1/\' | dmtxwrite -s 16x16 -o '
#            + fn_qr)

        # save data matrix code with unique id (python3 solution)
        fn, fext = os.path.splitext(self._fn)
        fn_qr = fn + '_qr' + '.png'

        uuid_str = str( uuid.uuid4() )
        uuid_str = uuid_str.replace('-','') # remove '-' from uuid
        uuid_str = uuid_str.lower() # make uuid lower case
        uuid_str = uuid_str[0:12] # first 12 bytes of uuid

        encoder = DataMatrixEncoder(uuid_str)
        encoder.save(fn_qr)
        
        self.cpt_rect['matrix'] = fn_qr
        

        # todo: rethink the following ...
        # two ways to organize addition of layers
        # delete all layers and reset them 
        # - in save function (any time file is saved, as done here)
        # - in setter function for self.cut (any time self.cut is changed)
        self.layer.remove_all()
        self.layer.add(
            pkg_resources.resource_filename(
                'schablone', 'templates/label/smd_container/' + self.label_type
                + '/font.svg'))

        if not self.cut:
            self.layer.add(
                pkg_resources.resource_filename(
                    'schablone', 'templates/label/smd_container/' +
                    self.label_type + '/frame.svg'))
        else:
            #			self.layer.default_lr = 'cut'
            self._fn_cut = super(smd_container, self)._fn_sub_str(self._fn,
                                                                  "_cut")
            self.layer.add(
                pkg_resources.resource_filename(
                    'schablone', 'templates/label/smd_container/' +
                    self.label_type + '/frame_cut.svg'), 0.0, 0.0, 1.0, 'cut')
            super(smd_container, self).save_layers(self._fn_cut, self._fn,
                                                   'cut')

        super(smd_container, self).save_layers()

        self.cpt_tspan['title'] = self.content.title
        self.cpt_tspan['value'] = self.content.value
        self.cpt_tspan['package'] = self.content.package
        self.cpt_tspan['tolerance'] = self.content.tolerance
        self.cpt_tspan[
            'temperature_coefficient'] = self.content.temperature_coefficient
        self.cpt_tspan['power'] = self.content.power
        super(smd_container, self).save_substitutes()

        #from cairosvg.surface import PDFSurface
        #PDFSurface.convert(src, write_to=open('output.pdf', 'w'))

    def saveAx(self, fn=None, ax='a4', svg_list=None):
        if svg_list is None:
            if self._fn_list == []:
                svg_list = []
                raise RuntimeError('List of svg_list is empty')
            else:
                svg_list = self._fn_list

#todo: raise error

        if fn == None:
            fn = "default_Ax.svg"

        cut = []
        cut_frame = []
        sans_cut = []

        for f in svg_list:
            f_cut = self._fn_sub_str(f, '_cut')
            if os.path.isfile(f_cut):
                cut.append(f)
                cut_frame.append(f_cut)
            else:
                sans_cut.append(f)

        fn_font = self._fn_sub_str(fn, '_print')
        fn_cut = self._fn_sub_str(fn, '_cut')

        super(smd_container, self).saveAx(fn, ax, sans_cut)
        super(smd_container, self).saveAx(fn_cut, ax, cut_frame)
        super(smd_container, self).saveAx(fn_font, ax, cut)


class box_content_container(object):
    def __init__(self):
        self.qr = ''
        self.title = ''
        self.project = ''
        self.editor = ''
        self.brief_content = ''
        self.location = ''


class box(generic):
    def __init__(self):
        super(box, self).__init__()

        self.content = box_content_container()

        self.fn_template_default = pkg_resources.resource_filename(
            'schablone', 'templates/label/box/template_default.svg')
        self.fn_template_extended = pkg_resources.resource_filename(
            'schablone', 'templates/label/box/template_extended.svg')

        self.label_type = 'default'
        #self.strict = False

    # hier wird die einzige Moeglichkeit der Basisklasse 
    # die Hoehe und Breite zu setzen ueberschrieben
    # Achtung ist überschreibend

    def save(self, fn=None):

        if fn == None:
            if self._fn == None:
                fn = "label_" + self.label_type + ".svg"
            else:
                fn = self._fn

        self._fn = fn

        # set width and height (reconfigure everytime time save is called)
        self.width = '88mm'
        if self.label_type == 'default':  # type "1" and type "1a" seem to have label same size
            self.height = '74mm'
        elif self.label_type == 'extended':
            self.height = '138mm'
        else:
            raise RuntimeError('Unknown type of label: ' + self.label_type)
        #self.height = '74mm'
        #self.label_type = 'default'

        super(box, self).save(fn)

        self.layer.add(
            pkg_resources.resource_filename(
                'schablone', 'templates/label/box/template_default.svg'))

        if self.label_type == 'extended':
            # save data matrix code with unique id (using bash)
            fn_qr = self._fn_sub_str(fn, '_qr')
            super(box, self).create_qr('http://www.sappz.de', fn_qr, 280, 20)

            self.layer.add(
                pkg_resources.resource_filename(
                    'schablone', 'templates/label/box/template_extended.svg'))

            #self.cpt_tspan['qr'] = self.content.qr
            self.cpt_tspan['id'] = self.content.qr

        self.cpt_tspan['title'] = self.content.title
        self.cpt_tspan['project'] = self.content.project
        self.cpt_tspan['editor'] = self.content.editor
        self.cpt_tspan['location'] = self.content.location
        self.cpt_flowpara['brief_content'] = self.content.brief_content

        super(box, self).save(fn)
