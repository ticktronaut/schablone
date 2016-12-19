#!/usr/bin/env python
#coding=utf-8

#import svgutils
import svgutils.transform as sg
import svglue
#import svgwrite
#import pysvg

from lxml import etree

import os

import pyqrcode

import pkg_resources

import base


class layer_container(object):
	def __init__(self, path, x=0.0, y=0.0, scale=1.0):
		self.x_pos = x 
		self.y_pos = y 
		self.scale = scale 
		self.path = path 

class layer_pack(object):
	def __init__(self):
		self.tmpl_lr={'default':[layer_container]*0}
		self.default_group='default' # todo: getter/setter for self.default_lr, wenn key nicht existiert  mindestens warning ...

	def add(self, path, x_pos=0.0, y_pos=0.0, scale=1.0, group=None):
		if group is None:
			group=self.default_group

		tmp=layer_container(path, x_pos, y_pos, scale)
		#self.tmpl_lr[group].append(tmp)
		self.tmpl_lr.setdefault(group,[]).append(tmp)

	def remove(self, nmb, group=None):
		if group is None:
			group=self.default_group
		elif group is 'all':
			print 'reset all layers'
	
		del self.tmpl_lr[group][nmb]

	def remove_all(self, group=None):
		if group is None:
			# remove all keys by resetting to default
			self.tmpl_lr={'default':[layer_container]*0}
		else:
			del self.tmpl_lr[group]

	def show(self, group=None):
		if group is None:
			group=self.default_group
		idx=0
		lrs=[]
		if group in self.tmpl_lr.keys():
			for lr in self.tmpl_lr[group]:
				lrs.append([idx, lr.path, lr.x_pos, lr.y_pos, lr.scale])
				idx +=1
	
			return lrs
		else:
			print 'todo: raise warning, key does not exist'

# Ueberlegung anstatt template-id evtl. direkt id verwenden
class generic(base.baseSVG):
	
	def __init__(self):
		super(generic, self).__init__()

		#self.qr_content = "http://www.sappz.de"

		# lists of paths to template layers
		# hier eigentlich dictionary von lists
		self.layer = layer_pack()
		self.__tmpl_layers=[]

		# captions
		self.cpt_tspan = {}
		self.cpt_flowpara = {}
		self.cpt_rect = {} #qr or img

	def create_sample(self):
		print "create svg"
		print "append captions"

	def create_qr(self, content, fn, x_pos, y_pos):
		# size depends on content
		qr = pyqrcode.create(content)#, version=17)
		qr.svg(fn)
		# todo: save, add layer
		self.layer.add(fn, x_pos, y_pos)

	def save_frame(self, fo=None):
		super(generic, self).save(fo)

	def save_layers(self, fo=None, fi=None, group=None):
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
		if fi==None:
			fi = self._fn
		if fo==None:
			fo = self._fn

		if group is None:
			group = self.layer.default_group

		tpl = svglue.load(file=self._fn)

		for cpt_key, cpt_val in self.cpt_tspan.iteritems():
			tpl.set_text(cpt_key, cpt_val)

		for cpt_key, cpt_val in self.cpt_flowpara.iteritems():
			tpl.set_flowtext(cpt_key, cpt_val)

		for cpt_key, cpt_val in self.cpt_rect.iteritems():
			tpl.set_image(cpt_key, file=cpt_val, mimetype='image/png')

		src = str(tpl)
		open(self._fn, 'w').write(src)
		#from cairosvg.surface import PDFSurface
		#PDFSurface.convert(src, write_to=open('output.pdf', 'w'))


	# hier wird die einzige Moeglichkeit der Basisklasse 
	# die Hoehe und Breite zu setzen ueberschrieben
	def save(self, fn = None):

		# save basic frame layer	
		self.save_frame(fn)
		# combine layers from template svg-files (svgutils)
		self.save_layers()
		# substitute text (svglue)
		self.save_substitutes()


#todo: saveAX(self, ax="a4", fn=None, svg_list=None):
#	def saveAx(self, fn=None, svg_list=None):
#		fn, fext = os.path.splitext(self._fnAx)	
#	def saveA4(self, fn=None, svg_list=None):
#		super(generic, self).saveA4(fn, svg_list)
#		fn, fext = os.path.splitext(self._fnA4)
#		fn_cut = fn + '_cut' + fext	
#		super(generic, self).saveA4(fn_cut, self._fn_cut_list)
