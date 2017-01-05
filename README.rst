=========
schablone
=========

What it is?
-----------

schablone is a library to create structured printed forms (svg format) and fill them with information. Its main purpose is to create labels for boxes in a storage system (for instance your local hacker space). Beyond that it is flexible enough to create many other structured documents, like for example resumes or business cards. Schablone broadly exploits the flexibility the xml formats, especially svg. In future development also other xml formats like html might be deployed. It relies on the libraries svglue, svgutils and lxml (currently indirectly). Occasionally also the library Rsvg (gi.repository) is utilized.

What can I use it for?
----------------------

schablone is a very flexible library to create structured svg files. The user must specify -template layers- of svg files with fields of images and text to fill in. The library stacks these layers and fills in the wished texts and images. The library might, for instance, be used to automize the creation of address labels in a django based e-commerce system.

.. figure:: images/smd_container.png
   :scale: 100 %

The library also can be used for some special tasks like creating box labels or labels of smd containers (as seen in the image above).

.. - create some of the schablone templates like
    - image samples box label
    - image samples smd container
 
.. - also generic labels can be created 

.. - some more generic labels may follow
    - link resume
    - business cards

Why should I use it?
--------------------

schablone simplifies the process of automatically creating labels and fill them in. Whenever structured documents should be created and filled in by python, schablone is a good workflow. Also the inclusion of qr-codes is supported (using the library pyqrcode_). The basic procedure is a three steps process:

.. _pyqrcode: https://pypi.python.org/pypi/PyQRCode/1.2.1

1. `store frame SVG file which has the wished size`_
2. `stack layers of svg file templates`_
3. `fill in texts and images`_

.. figure:: images/layers.png
   :scale: 70 %


Usage
-----

store frame SVG file which has the wished size
``````````````````````````````````````````````
   
tbc
   
stack layers of svg file templates
``````````````````````````````````

tbc   
   
   
fill in texts and images 
````````````````````````
   
tbc
save A4
   
Examples
--------

In the following some example on using the examples are given. A more detailed example, concluding all these examples can be found in sample.py.
   
Create generic label
````````````````````

schablone can create generic templates. The result can be seen in samples/generic/generic.svg.

::

    import schablone.generic

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
    genLabel.layer.add('tmpl_layer/tmpl_layer_2.svg')
    fn = generic_label_dir + '/generic_qr.svg'
    genLabel.create_qr('http://www.sappz.de', fn, 160, 160)
    
    genLabel.layer.remove(1)
    fn = generic_label_dir + '/' + 'generic.svg'
    genLabel.save(fn)

Create smd container
````````````````````

There are also some specialized applications of schablone. One of them is to create labels for **mira** smd containers. Exemplary outputs can be found in the image in chapter `What can I use it for?`_.

::

    import schablone.label

    if not os.path.exists(single_dir):
        os.makedirs(single_dir)

    smdLabel = schablone.label.smd_container()
    smdLabel.overwrite = True
    smdLabel.cut = False # if True, the frame is 
                         # put in a separate file
                         # in red (for laser cutter).
    smdLabel.content.title = 'SMD-Wid.'
    smdLabel.content.package = '0805'
    smdLabel.content.tolerance = '1%'
    smdLabel.content.temperature_coefficient = 'TK100'
    smdLabel.power = '1/8W'

    smdLabel.content.value = '120k' 
    fn = single_dir + '/' + 'smd_caption_' + '120k' + '.svg'
    smdLabel.save(fn)

    smdLabel.content.value = '180k'
    fn = single_dir + '/' + 'smd_caption_' + '180k' + '.svg'
    smdLabel.save(fn)


Create box label 
````````````````

Another special application is the creation of box labels. The exemplary result can be seen in samples/box_label/default_label.svg.

::

    import schablone.label

    if not os.path.exists(box_label_dir):
        os.makedirs(box_label_dir)

    boxLabel = schablone.label.box()
    boxLabel.overwrite = True
    boxLabel.content.title = 'Ein Box Label'
    boxLabel.content.project = 'Projekt A'
    boxLabel.content.editor = 'A.G.'
    boxLabel.content.location = 'Regal A, Reihe A'
    boxLabel.content.brief_content = 'Einige Dinge die sich in der Box befinden ...'
    fn = box_label_dir + '/' + 'default_label.svg'
    boxLabel.save(fn)
    boxLabel.label_type = 'extended'
    vn = box_label_dir + '/' + 'extended_label.svg'
    boxLabel.save(fn)

Save history of stored files in one A4 file
```````````````````````````````````````````

The function ----todo: link to function reference----- saves the history of all stored svg files in one DIN format file. The following example shows this on smd containers.

::

    import schablone.label

    if not os.path.exists(single_dir):
        os.makedirs(single_dir)

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

Requirements
------------

It relies on the libraries 

* svglue_,
* svgutils_
* and lxml_ (currently indirectly). 

.. _svglue: https://pypi.python.org/pypi/svglue/0.2.1
.. _svgutils: https://pypi.python.org/pypi/svgutils/0.2.0
.. _lxml: https://pypi.python.org/pypi/lxml/3.7.1 

Occasionally also the library **Rsvg** (gi.repository) is utilized. Installation using pip and aptitude (tested on Ubuntu 14.04): ::

    $ pip install svglue svgutils lxml 
    $ apt-get install gir1.2-rsvg-2.0 python3-cairo

Installation
------------

::

    $ pip install schablone 

License
-------

todo 
