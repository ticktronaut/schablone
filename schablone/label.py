#!/usr/bin/env python
#coding=utf-8

import os
import svgutils.transform as sg
import svglue
import uuid
import pyqrcode
from lxml import etree
import pkg_resources
from pystrich.datamatrix import DataMatrixEncoder
from .generic import *

import logging

log = logging.getLogger("schablone.label")

class smd_content_container(object): #FixMe cap_content_container | res_content_container support
    def __init__(self):
        log.debug("Instantiating class 'smd_content_container'.")
        self.title = ''
        self.value = ''
        self.package = ''
        self.tolerance = ''
        self.temperature_coefficient = ''
        self.power = ''


class smd_container(generic):

    def __init__(self, label_type='mira_1', tmpl_path=None, size=None, cut=False):
        
        super(smd_container, self).__init__()
 
        self._fn_cut = ''
        self.content = smd_content_container()

        if tmpl_path is None: # set default template path
            self.tmpl_path = pkg_resources.resource_filename('schablone', 'templates') + '/label/smd_container'
        else:
            self.tmpl_path = tmpl_path
            self.content._is_custom_template = True

#        self.label_type = label_type  #todo: link zu quelle #getter setter: remove all layers, reset layers
#        self.cut = False  #todo getter setter: remove all layers, reset layers

        # todo: Ueber Funktion nachdenken
        self.label_types = ('mira_1', 'licefa_n1') # tuple with valid label types (create getter?) 

        if size is not None:
            if len(size) != 2:
                raise RuntimeError("list of len 2 required (x,y)")
            self.width = size[0]
            self.height = size[1]

        self.cpt_tspan = {
            'title': '',
            'value': '',
            'package': '',
            'tolerance': '',
            'temperature_coefficient': '',
            'power': ''
            # FixMe: Add voltage
        }
        #self.cpt_flowpara = {}
        self.cpt_rect = {'matrix': ''}

        # layers are set here
        self._set_layers(label_type, cut)

        if label_type == 'mira_1' or label_type == 'mira_1a':  # type "1" and type "1a" seem to have the same label size
            self.width = '15mm'
            self.height = '20mm'
        elif label_type == 'mira_2':
            raise RuntimeError('Label type mira_2 not supported, yet.')
        elif label_type == 'mira_3':
            raise RuntimeError('Label type mira_3 not supported, yet.')
        elif label_type == "mira_4":
            raise RuntimeError('Label type mira_4 not supported, yet.')
        elif label_type == 'licefa_n1': # SMD-Box N1
            raise RuntimeError('Label type licefa_n1 not supported, yet.')
            self.width = '22mm'
            self.height = '29mm'
        elif label_type == 'licefa_n2': # SMD-Box N2
            raise RuntimeError('Label type licefa_n2 not supported, yet.')
            self.width = '29mm'
            self.height = '42mm'
        elif label_type == 'licefa_n3': # SMD-Box N3
            raise RuntimeError('Label type licefa_n2 not supported, yet.')
            self.width = '42mm'
            self.height = '56mm'
        else:
            # No standard label type found, so must be custom type.
            # Check if a custom template path is specified, otherwise raise error.
            log.debug("Attempt to use custom label type '" + label_type + "'")
            if not self.content._is_custom_template:
                log.error("Please specify template path to custom label type.")
                raise RuntimeError("Please specify template path to custom label type.")
            # FixMe: use size from parameter
            print(self.width)
            print(self.height)


    def _set_layers(self, label_type, cut=None):

        if cut is None:
            cut=True

        self.layer.clear('smd_container_font')
        self.layer.clear('smd_container_matrix')
        self.layer.clear('smd_container_frame')
        self.layer.clear('smd_container_cut')

        path = self.tmpl_path + '/' + label_type

        self.layer.add(path + '/font.svg', group='smd_container_font')
        self.layer.add(path + '/matrix.svg', group='smd_container_matrix')
        if not cut:
            self.layer.add(path + '/frame.svg', group='smd_container_frame')
        else:
            #self._fn_cut = super(smd_container, self)._fn_sub_str(self._fn, "_cut")
            self.layer.add(path + '/frame_cut.svg', group='smd_container_cut')
            #super(smd_container, self).save_layers(self._fn_cut, self._fn, 'cut')



    # hier wird die einzige Moeglichkeit der Basisklasse 
    # die Hoehe und Breite zu setzen ueberschrieben
    # Achtung ist überschreibend
    def save(self, fn=None):
        # Currently all other parameters are set in __init__()
 
        if fn is not None:
            self._fn = fn

        # todo check if ... in self.cpt_tspan.keys():
        self.cpt_tspan['title'] = self.content.title
        self.cpt_tspan['value'] = self.content.value
        self.cpt_tspan['package'] = self.content.package
        self.cpt_tspan['tolerance'] = self.content.tolerance
        self.cpt_tspan['temperature_coefficient'] = self.content.temperature_coefficient
        self.cpt_tspan['power'] = self.content.power

        # self.fn is set after this point 
        # todo: think about better solution for self._fn (explicit is better than implicit) 
        super(smd_container, self).save_frame(fn)

        self._fn_cut = super(smd_container, self)._fn_sub_str(self._fn,
                                                              '_cut')

        # save data matrix code with unique id (python3 solution)
        fn, fext = os.path.splitext(self._fn)
        fn_qr = fn + '_qr' + '.png'

        uuid_str = str( uuid.uuid4() )
        uuid_str = uuid_str.replace('-','') # remove '-' from uuid
        uuid_str = uuid_str.lower() # make uuid lower case
        uuid_str = uuid_str[0:12] # first 12 bytes of uuid

        encoder = DataMatrixEncoder(uuid_str)
        encoder.save(fn_qr)

        if 'matrix' in self.cpt_rect.keys():
            self.cpt_rect['matrix'] = fn_qr

        # save layers
        for group in self.layer.tmpl_lr.keys():
            if group == 'smd_container_cut':
                super(smd_container, self).save_layers(self._fn_cut, self._fn, 'smd_container_cut')
            else:
                super(smd_container, self).save_layers(group=group)

        # save substitutes
        super(smd_container, self).save_substitutes()

        # FixMe: park following code in script or documentation
        #from cairosvg.surface import PDFSurface
        #PDFSurface.convert(src, write_to=open('output.pdf', 'w'))

    def saveAx(self, fn=None, ax='a4', svg_list=None):
        if svg_list is None:
            if self._fn_list == []:
                svg_list = []
                raise RuntimeError('List of svg_list is empty')
            else:
                svg_list = self._fn_list

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
        log.debug("Instantiating class 'box_content_container'.")
        self.qr = ''
        self.title = ''
        self.project = ''
        self.editor = ''
        self.brief_content = ''
        self.location = ''


class box(generic):
    def __init__(self):
        log.debug("Instantiating class 'box'.")
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
            self.height = '74mm'
        else:
            raise RuntimeError('Unknown type of label: ' + self.label_type)
        #self.height = '74mm'
        #self.label_type = 'default'

        super(box, self).save(fn)

        self.layer.clear()

        self.layer.add(
            pkg_resources.resource_filename(
                'schablone', 'templates/label/box/template_default.svg'))

        if self.label_type == 'extended':
            # save data matrix code with unique id (using bash)
            fn_qr = self._fn_sub_str(fn, '_qr')
            super(box, self).create_qr(self.content.qr, fn_qr, 280, 220)

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
