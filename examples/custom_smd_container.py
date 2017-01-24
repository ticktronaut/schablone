#!/usr/bin/env python
#coding=utf-8

import os

#import schablone
import schablone.label
import schablone.generic
import schablone.label

from pystrich.datamatrix import DataMatrixEncoder

base_dir = 'samples'
custom_dir = base_dir + '/' + 'smd_conteiner' + '/' + 'custom_smd_container'
fn = custom_dir + '/' + 'smd_label.svg'

if not os.path.exists(custom_dir):
    os.makedirs(custom_dir)

smdLabel = schablone.label.smd_container(label_type='mira_1', cut=False)
smdLabel.overwrite = True
#smdLabel.cut = False
#smdLabel.matrix = False
smdLabel.content.title = 'SMD-Wid.'
smdLabel.content.package = '0805'
smdLabel.content.tolerance = '1%'
smdLabel.content.temperature_coefficient = 'TK100'
smdLabel.power = '1/8W'
smdLabel.content.value = '120k'
print('hieeeeeeeeeeeeeeeeeeeeeeeeeeeeeeer: ')
print( smdLabel.layer.show('smd_container_matrix') )
smdLabel.layer.clear('smd_container_matrix')
smdLabel.layer.add('tmpl_layer/cstm_layer.svg')

encoder = DataMatrixEncoder('rs    2132547')
encoder.save('data_matrix.png')

del smdLabel.cpt_rect['matrix']

smdLabel.cpt_rect = {'custom_matrix': 'data_matrix.png'}
smdLabel.save(fn)
