============
Architecture
============

The base functionality is provided in the base class:
    * Create and save svg files.
    * Manage overwriting of files (if overwrite is not wished the class can check if a file with the given filename exists already. If so the filename is extended with a consecutive index (<filename>_index.svg)
    * Keep track of the paths to all stored files.
    * Store history of stored files to one DIN format file. If the size expands one page, more files with page indexes are stored.

Diagram
-------
::

                                       
                                      +-----------+
                                      |           |
                                      |   base    |
                                      +-----------+   
                                            |
                                      +-----------+
                                      |           |
                                      |  generic  |
                                      +-----------+     
                                           |
             +--------------+--------------+ 
             |              |
       +--------+     +-----------+                                               
       |  box   |     |  smd      |                            
       |  label |     | container |                    
       +--------+     +-----------+                       
