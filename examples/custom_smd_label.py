#!/usr/bin/env python
#coding=utf-8

"""
This example shows how to generate custom labels for SMD container with
a user specified template path.
"""

import os
import schablone
import schablone.label

base_dir = 'samples'
single_dir = base_dir + '/smd_container/custom_smd_label/' + 'smd_container'

if not os.path.exists(single_dir):
    os.makedirs(single_dir)

user_tmpl_path = '/path/to/schablone/examples/tmpl_layer' # FixMe: currently works only with absolute path
custom_tmpl_path = '/home/usappz/make/code_projects/schablone/examples/tmpl_layer' # FixMe: currently works only with absolute path
smdLabel = schablone.label.smd_container(label_type='my_custom_label', tmpl_path=custom_tmpl_path, size=['15mm','20mm'] )
smdLabel.overwrite = True
smdLabel.cut = False
smdLabel.content.title = 'SMD-Wid.'
smdLabel.content.package = '0805'
smdLabel.content.tolerance = '1%'
smdLabel.content.temperature_coefficient = 'TK100'
smdLabel.power = '1/8W'
smdLabel.content.value = '120k'
fn = single_dir + '/' + 'smd_caption_' + smdLabel.content.value + '.svg'
smdLabel.save(fn)
