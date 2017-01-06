#!/usr/bin/env python
#coding=utf-8

from lxml import etree
import svgutils.transform as sg

#import rsvg
import gi
gi.require_version('Rsvg', '2.0') # FixMe: select required version to supress warning
from gi.repository import Rsvg # gi.repository is a special Python package that dynamically generates objects

import os
import warnings


class baseSVG(object):
    """Functionality for basic SVG-File creation.

    The class **baseSVG** is able to store basic empty SVG files of given width 
    and height. Files can be stored by the save() method. If the attribute 
    overwrite is set False, overwriting files is prevented, by extending the 
    filename with an index.

    Every instance of **baseSVG** keeps track on the history of all paths to
    formerly stored files using save(). By saveAx() all these files (or a custom
    set of files) can be arranged in a DIN-format file. If the arrangement of
    the files expands the page size of the DIN file, a new file for a new page 
    is stored.

    Example
    -------
    ::    

        from base import baseSVG
     
        sample_svg = baseSVG() 
        sample_svg.width = '20mm'
        sample_svg.height = '20mm'
        sample_svg.save('sample.svg')

    Note
    ----
    **baseSVG** class is used as base functionality for the class **generic**. 
    All further derived classes are children of **generic**.

    Attributes
    ----------
    description : str
        Optional description of the svg file. 
    author : str
        Optional author of the file.
    version : str
        Optional version of the file. 
    width : str
        width of the file - exemplary formats (compatible with SVG standard): "500" or "500px", "132mm"
    height : str 
        height of the file - exemplary formats (compatible with SVG standard): "500" or "500px", "132mm"
    _fn : str
        Filename of the svg corresponding file.
    _fnAx : str
        Filename of svg file to gather formerly stored svg files.
    landscapeAx : bool
        Format for _fnAx file.
    _svg_content : str
        Content of the svg file. it is not recommended to change this. 

    """

    def __init__(self):
        self.description = "" 
        self.author = ""
        self.version = 0.1

        #todo: write getter/setter with better control
        #on svg-compatible layout of width and height
        self.width = "500"
        self.height = "500"

        self._fn = None
        # self._fnA4 = None
        self._fnAx = None
        self._fn_list = []

        self.landscapeAx = True

        self.overwrite = False

        #todo: viewBox="0 0 100 100"
        self._svg_content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"" + str(
            self.width) + "\" height=\"" + str(self.height) + "\">\n</svg>"

        #self.__create(fn, overwrite)

    def _check_fn_exists(self, fn):
        """Check if filename exists. If so, extend the filename with an index.
  
        Parameters
        ----------
        fn
            Filename to be checked for existence. 

        """

        ext = 0
        fp, fe = os.path.splitext(fn)
        fn_tmp = fn
        while os.path.isfile(fn_tmp):
            ext += 1
            fn_tmp = fp + '_' + str(ext) + fe

        return fn_tmp

    def _fn_sub_str(self, fn, sub_str):
        """Place a substring between filename and extension.
  
        Parameters
        ----------
        fn 
            Filename to be extended. 
        sub_str
            Substring to be placed between filename and extension.

        """

        fnbase, fext = os.path.splitext(fn)
        return fnbase + sub_str + fext

    def __create(self, fn, width="500", height="500"):
        # alternativer Ansatz: 
        # existiert bereits ein SVG-Label, pruefen, ob es sich um ein SVG-Label handelt
        # und dessen Werte in Klassenrumpf (etree) übernehmen  
        ext = 0
        self._fn = fn
        self._svg_content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"" + str(
            width) + "\" height=\"" + str(height) + "\">\n</svg>"
        if fn.endswith('.svg'):
            if not self.overwrite:
                # alternativer Ansatz: 
                # existiert bereits ein SVG-Label, prüfen, ob es sich um ein SVG-Label handelt
                # und dessen werte in Klassenrumpf übernehmen
                #tree = etree.parse(self._fn)
                #self._svg_root = tree.getroot()
                #if contains pySVGfile:
                #   Daten in Klassenrumpf übernhemen
                fn = self._check_fn_exists(fn)

            self._fn = fn

            try:
                file = open(fn, 'w')
                file.write(self._svg_content)
                file.close()
            except:
                raise RuntimeError('Could not create/open file ' + fn)

        else:
            raise RuntimeError('File extension must be a valid svg file.')

    def save(self, fn=None):
        """Store content to svg-file.
  
        Note
        ----
        The save function may be called more than once, with different filenames.

        Parameters
        ----------
        fn
            Filename of the saved file. If left blank, the filename of the previously saved file is taken. 
            If there is no filename, it defaults to default.svg. The filename will be stored in the _fn 
            class member.

        """
        if fn == None:
            if self._fn == None:
                self._fn = "defaul.svg"
        else:
            self._fn = fn

        self.__create(self._fn)

        tree = etree.parse(self._fn)
        root = tree.getroot()

        root.attrib["height"] = str(self.height)
        root.attrib["width"] = str(self.width)

        tree.write(self._fn)

        self._fn_list.append(self._fn)

    def saveAx(self, fn=None, ax='a4', svg_list=None):
        """Store history of previously files in a DIN-format file.

        Note
        ----
        In the optional parameter svg_list, a custom list of file paths may be used instead of the 
        history of previously stored files.

        Parameters
        ----------
        fn
            Filename of the saved file. If left blank, the filename defaults to the existing filename 
            saved in the class members. If there is no filename, it defaults to default_Ax.svg. 
            The filename will be stored in the _fnAx class member.
        ax
            String to define the size of the DIN format document. Allowed is 'a0', 'a1', ..., 'a10'.
        svg_list
            Custom list of paths to files, which should be aranged to the DIN format svg file. By default 
            the history of paths to all files stored by the save() function, stored in the class member 
            _fn_list is stored.
        
        """
        widthAx = {
            'a10': 92,
            'a9': 131,
            'a8': 184,
            'a7': 262,
            'a6': 372,
            'a5': 524,
            'a4': 744,
            'a3': 1052,
            'a2': 1488,
            'a1': 2104,
            'a0': 2979
        }
        heightAx = {
            'a10': 131,
            'a9': 184,
            'a8': 262,
            'a7': 372,
            'a6': 524,
            'a5': 524,
            'a4': 1052,
            'a3': 1488,
            'a2': 2104,
            'a1': 2979,
            'a0': 4212
        }
        if svg_list == None:
            if self._fn_list == []:
                warnings.warn(
                    'svg_list is empty. No files available to store to Ax file.'
                )
                svg_list = []
            else:
                svg_list = self._fn_list

        if fn == None:
            fn = "default_Ax.svg"

        if not self.overwrite:
            fn = self._check_fn_exists(fn)

        self._fnAx = fn

        if self.landscapeAx:
            width = heightAx[ax] 
            height = widthAx[ax] 
        else:
            width = widthAx[ax]  
            height = heightAx[ax] 

        pg_nmb = 0
        self._fnAx = self._fn_sub_str(fn, ('_pg' + str(pg_nmb)))
        self.__create(self._fnAx, width, height)

        x_pos = 0
        y_pos = 0

        svg_label = sg.fromfile(self._fnAx)

        # derzeit noch suboptimal, da nur gut fuer gleich Hoehen (todo: besseren Algorithmus entwickeln)
        for svg_file in svg_list:
            handle = Rsvg.Handle()
            svg = handle.new_from_file(svg_file)
            h = svg.get_dimensions().height
            w = svg.get_dimensions().width
            #rsvg_anker = Rsvg.Handle(file=svg_file)
            #(w, h, w2, h2) = rsvg_anker.get_dimension_data()
            anker = sg.fromfile(svg_file).getroot()
            anker.moveto(x_pos, y_pos, scale=1.0)
            svg_label.append(anker)

            if (width - (x_pos + w)) > w:
                x_pos += w
            else:
                if (height - (y_pos + h)) > h:
                    y_pos += h
                    x_pos = 0
                else:  # new page
                    # store current page -> todo: check if file exists
                    svg_label.save(self._fnAx)
                    # reset positions
                    x_pos = 0
                    y_pos = 0
                    # increase page number
                    pg_nmb += 1
                    # create new page
                    self._fnAx = self._fn_sub_str(fn, ('_pg' + str(pg_nmb)))
                    self.__create(self._fnAx, width, height)
                    svg_label = sg.fromfile(self._fnAx)

            #if h>max_height:
            #	max_height=h

        self._fnAx = self._fn_sub_str(fn, ('_pg' + str(pg_nmb + 0)))
        svg_label.save(self._fnAx)
