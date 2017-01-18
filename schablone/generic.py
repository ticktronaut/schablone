#!/usr/bin/env python
#coding=utf-8

import os
import svgutils.transform as sg
import svglue
from lxml import etree
import pyqrcode
import pkg_resources
from .base import baseSVG

import logging

import warnings

log = logging.getLogger('schablone.generic')

class layer_container(object):
    def __init__(self, path, x=0.0, y=0.0, scale=1.0):
        log.debug("Instantiating class 'layer_container'.")
        self.x_pos = x
        self.y_pos = y
        self.scale = scale
        self.path = path


class layer_pack(object):
    def __init__(self):
        log.debug("Instantiating class 'layer_pack'.")
        self.tmpl_lr = {'default': [layer_container] * 0}
        self.default_group = 'default'  # todo: getter/setter for self.default_lr, wenn key nicht existiert  mindestens warning ...

    def add(self, path, x_pos=0.0, y_pos=0.0, scale=1.0, group=None):
        if group is None:
            group = self.default_group

        tmp = layer_container(path, x_pos, y_pos, scale)
        #self.tmpl_lr[group].append(tmp)
        self.tmpl_lr.setdefault(group, []).append(tmp)

    def remove(self, nmb, group=None):
        if group is None:
            group = self.default_group
        elif group is 'all':
            pass
            #print 'reset all layers'

        del self.tmpl_lr[group][nmb]

    def clear(self, group=None):
        if group is None:
            # remove all keys by resetting to default
            self.tmpl_lr = {'default': [layer_container] * 0}
        else:
            del self.tmpl_lr[group]

    def show(self, group=None):
        if group is None:
            group = self.default_group
        idx = 0
        lrs = []
        if group in self.tmpl_lr.keys():
            for lr in self.tmpl_lr[group]:
                lrs.append([idx, lr.path, lr.x_pos, lr.y_pos, lr.scale])
                idx += 1

            return lrs
        else:
            pass
            # raise warning
            #print 'todo: raise warning, key does not exist'


class generic(baseSVG):
    """Stack layers svg file templates and replace text.

    The **generic** class contains core functionality of the **schablone** 
    library. It can create SVG files from sets of SVG file templates and 
    fill them in with text. Though, the steps (exceppt the first step) may 
    be mixed and executed redundantly, in general this is a three step process:

    1. store frame SVG file 
    2. stack layers of svg file templates 
    3. fill in texts and images 

    **generic** inherits from **baseSVG**.

    For stacking the template layers, **schablone** depends on svgutils. To fill
    the resulting file with content the texts are substituted. For this purpose
    svglue is being used. The Templates containing content intended to be filled in,
    must have tags representing them (rect, tspan, flowpara) with a custom attribute
    template-id. Each template-id must have a unique identifier. These identifiers
    are represented by the class members cpt_tspan, cpt_flowpara, cpt_rect.
    
    Example
    -------
    ::    

        import schablone.generic 
   
        generic_svg = schablone.generic.generic() 
        generic_svg.overwrite = True 
        genLabel.width = '200'
        genLabel.height = '200'
        genLabel.cpt_tspan['static_txt'] = u'Replace some text here.'
        genLabel.cpt_flowpara['flow_txt'] = u'Also flow text may be replaced.'
        genLabel.layer.add('tmpl_layer/tmpl_layer_1.svg')
        genLabel.layer.add('tmpl_layer/tmpl_layer_2.svg')
        genLabel.layer.add('tmpl_layer/tmpl_layer_2.svg')
        genLabel.create_qr('http://www.samp.le', 'qr.svg', 160, 160)
        genLabel.layer.remove(1)
        genLabel.save('sample.svg')

    Note
    ----
    The **generic** class contains the core functionality of **schablone**. All further 
    classes are derived from **generic**.

    Attributes
    ----------
    layer : layer_pack()
        Paths to the layers of templates. 
    cpt_span : dictionary 
        Pairs of name of the template-id and the corresponding text intended to substitute.
    cpt_flowpara : dictionary 
        Pairs of name of the template-id and the corresponding text intended to substitute.
    cpt_rect : dictionary 
        Pairs of name of the template-id and the corresponding path to the image intended 
        to substitute.

    """

    def __init__(self):
        log.debug("Instantiating class 'generic'.")
        super(generic, self).__init__()

        # lists of paths to template layers
        self.layer = layer_pack()

        # captions
        self.cpt_tspan = {}
        self.cpt_flowpara = {}
        self.cpt_rect = {}  #qr or img

    def create_sample(self):
        """Not implemented, yet."""
        pass

    def create_qr(self, content, fn, x_pos, y_pos):
        """Save qr-code, which can be used as template.

        Stores a qr-code and adds it to the layers by layer.add.
  
        Parameters
        ----------
        content 
            Content of the qr-code. 
        fn
            Filename of the qr-code SVG template. 
        x_pos
            Intended x-position of the layer. 
        y_pos
            Intended y-position of the layer. 

        """ 
        # size depends on content
        qr = pyqrcode.create(content)  #, version=17)
        qr.svg(fn)
        # todo: save, add layer
        self.layer.add(fn, x_pos, y_pos)

    def save_frame(self, fo=None):
        """Save the frame SVG-file.

        Note
        ----
            This is the basic frame of the SVG file. It is recommended to be called only once per file, 
            except you know what you do.

        
        """
        super(generic, self).save(fo)

    def save_layers(self, fo=None, fi=None, group=None):
        """Stack all template layers to the frame SVG file.

        Note
        ----
            In most cases it is convenient to skip the arguments fi and fo.
  
        Parameters
        ----------
        fo 
            Output filename (defaults to classmember _fn). 
        fi
            Input filename (defaults to classmember _fn). 
        group 
            Template layer group. Defaults to classmember default_group. 

        """ 
        if fi is None:
            fi = self._fn
        if fo is None:
            fo = self._fn

        if group is None:
            group = self.layer.default_group

        # combine svg-files 
        svg_label = sg.fromfile(fi)
        for layer in self.layer.tmpl_lr[group]:
            anker = sg.fromfile(layer.path).getroot()
            anker.moveto(layer.x_pos, layer.y_pos, layer.scale)
            svg_label.append(anker)

        svg_label.save(fo)

    def save_substitutes(self, fo=None, fi=None, group=None):
        """Substitute texts and store the substitutions to SVG file.
 
        Note
        ----
            In most cases it is convenient to skip the arguments fi and fo.
     
        """
        log.debug("Substitute text and store to SVG file.")
        if fi == None:
            fi = self._fn
        if fo == None:
            fo = self._fn

        if group is None:
            group = self.layer.default_group

        tpl = svglue.load(file=self._fn)

        for cpt_key, cpt_val in self.cpt_tspan.items():
            try:
                tpl.set_text(cpt_key, cpt_val)
            except:
                warnings.warn(
                    'Something went wrong setting the key \'' + cpt_key + '\'',
                    RuntimeWarning
                )
                # think about self.strict

        for cpt_key, cpt_val in self.cpt_flowpara.items():
            try: 
                tpl.set_flowtext(cpt_key, cpt_val)
            except:
                warnings.warn(
                    'Something went wrong setting the key ' + cpt_key + '\'',
                    RuntimeWarning
                )
                # think about self.strict

        for cpt_key, cpt_val in self.cpt_rect.items():
            try:
                tpl.set_image(cpt_key, file=cpt_val, mimetype='image/png')
            except:
                warnings.warn(
                    'Something went wrong setting the key \'' + cpt_key + '\'',
                    RuntimeWarning
                )
                # think about self.strict


        src = tpl.__str__()  #str(tpl) #str(tpl) does not work in python3
        open(self._fn, 'wb').write(src)
        #from cairosvg.surface import PDFSurface
        #PDFSurface.convert(src, write_to=open('output.pdf', 'w'))

    # hier wird die einzige Moeglichkeit der Basisklasse 
    # die Hoehe und Breite zu setzen ueberschrieben

    def save(self, fn=None):

        # save basic frame layer	
        self.save_frame(fn)
        # combine layers from template svg-files (svgutils)
        self.save_layers()
        # substitute text (svglue)
        self.save_substitutes()

