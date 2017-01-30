#!/usr/bin/env python
#coding=utf-8

import os

#import schablone
import schablone.label
import schablone.generic
import schablone.label

base_dir = 'samples'
smd_container_dir = base_dir + '/' + 'smd_container'
box_label_dir = base_dir + '/' + 'box_label'
generic_label_dir = base_dir + '/' + 'generic'
single_dir = smd_container_dir + '/' + 'single_files'
Ax_dir = smd_container_dir + '/'  +'Ax_files'

if not os.path.exists(single_dir):
    os.makedirs(single_dir)

if not os.path.exists(Ax_dir):
    os.makedirs(Ax_dir)

if not os.path.exists(box_label_dir):
    os.makedirs(box_label_dir)

if not os.path.exists(generic_label_dir):
    os.makedirs(generic_label_dir)

genLabel = schablone.generic.generic()
genLabel.overwrite = True
genLabel.width = '200'
genLabel.height = '200'
genLabel.cpt_tspan['static_txt'] = u'Replace some text here.'
genLabel.cpt_flowpara['flow_txt'] = u'Also flow text may be replaced.'
genLabel.layer.add('tmpl_layer/tmpl_layer_1.svg')
genLabel.layer.add('tmpl_layer/tmpl_layer_2.svg')
fn = generic_label_dir + '/generic_qr.svg'
genLabel.create_qr('http://www.sappz.de', fn, 160, 160)

#print genLabel.layer.show()
#genLabel.layer.remove(1)
#print genLabel.layer.show()
fn = generic_label_dir + '/' + 'generic.svg'
genLabel.save(fn)

smdLabel = schablone.label.smd_container()
smdLabel.overwrite = True
smdLabel.cut = True
smdLabel.content.title = 'SMD-Wid.'
smdLabel.content.package = '0805'
smdLabel.content.tolerance = '1%'
smdLabel.content.temperature_coefficient = 'TK100'
smdLabel.power = '1/8W'

res_e12 = [
    '1', '1.2', '1.5', '1.6', '1.8', '2.2', '2.7', '3.3', '3.9', '4.7', '5.6',
    '6.8', '8.2', '10', '12', '15', '18', '22', '27', '33', '39', '47', '56',
    '68', '82', '100', '120', '150', '180', '220', '270', '330', '390', '470',
    '560', '680', '820', '1k', '1k2', '1k5', '1k8', '2k2', '2k7', '3k3', '3k9',
    '4k7', '5k6', '6k8', '8k2', '10k', '12k', '15k', '18k', '22k', '27k',
    '33k', '39k', '47k', '56k', '68k', '82k', '100k', '120k', '150k', '180k',
    '220k', '330k', '390k', '470k', '560k', '680k', '820k'
]
cap = ['100n']
cpt_vals = res_e12 + cap

for val in cpt_vals:
	smdLabel.content.value = val
	fn = single_dir + '/' + 'smd_caption_' + val + '.svg'
	smdLabel.save(fn)

din = 'a4'
fn_Ax = Ax_dir + '/' + din + '.svg'
smdLabel.saveAx(fn_Ax, din)

boxLabel_default = schablone.label.box(label_type='default')
boxLabel_default.overwrite = True
boxLabel_default.content.title = 'Ein Box Label'
boxLabel_default.content.project = 'Projekt A'
boxLabel_default.content.editor = 'A.G.'
boxLabel_default.content.location = 'Regal A, Reihe A'
boxLabel_default.content.brief_content = 'Einige Dinge die sich in der Box befinden ...'
fn = box_label_dir + '/' + 'default_label.svg'
boxLabel_default.save(fn)


boxLabel_extended = schablone.label.box(label_type='extended')
boxLabel_extended.overwrite = True
boxLabel_extended.content.title = 'Ein Box Label'
boxLabel_extended.content.project = 'Projekt A'
boxLabel_extended.content.editor = 'A.G.'
boxLabel_extended.content.location = 'Regal A, Reihe A'
boxLabel_extended.content.brief_content = 'Einige Dinge die sich in der Box befinden ...'
boxLabel_extended.content.qr = 'test'
fn = box_label_dir + '/' + 'extended_label.svg'
boxLabel_extended.save(fn)
